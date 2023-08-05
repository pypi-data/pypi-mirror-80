import errno
import json
import os
import time

from ask_sdk_core.attributes_manager import AttributesManager
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill import CustomSkill
from ask_sdk_core.view_resolvers import TemplateFactory
from ask_sdk_model import RequestEnvelope, ResponseEnvelope
from ask_sdk_model.services import ServiceClientFactory, ApiConfiguration
from ask_sdk_runtime.exceptions import AskSdkException
from ask_smapi_model.v1.skill.simulations.device import Device
from ask_smapi_model.v1.skill.simulations.input import Input
from ask_smapi_model.v1.skill.simulations.simulations_api_request import SimulationsApiRequest
from ask_smapi_sdk import StandardSmapiClientBuilder


class TestResponse:
    def __init__(self, event=None, lambda_function=None, response: ResponseEnvelope = None):
        self.event = event
        self.lambda_function = lambda_function
        self.response = response


class SkillTester:

    def __init__(self, sb, location="pt-BR", request_folder="/tmp/ask_test", client_id=None, client_secret=None,
                 refresh_token=None, skill_id=None, default_location=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.skill_id = skill_id
        self.default_location = default_location
        smapi_client_builder = StandardSmapiClientBuilder(client_id=self.client_id, client_secret=self.client_secret,
                                                          refresh_token=self.refresh_token)
        self.smapi_client = smapi_client_builder.client()
        self.skill = CustomSkill(skill_configuration=sb.skill_configuration)
        s = self.smapi_client.get_skill_status_v1(self.skill_id)
        self.tag = s.to_dict()['interaction_model'][location]['e_tag']
        self.request_folder = request_folder + "/" + self.tag + "/"

        try:
            os.makedirs(os.path.dirname(self.request_folder), exist_ok=True)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    def check_if_request_exist(self, input_text, session, prefix=""):
        h = "{}_{}_{}".format(prefix, hash(input_text), hash(str(session)))
        file_name = "{}/{}.json".format(self.request_folder, h)
        if os.path.isfile(file_name):
            with open(file_name) as file:
                return json.load(file)
        else:
            return None

    def save_request(self, input_text, session, request_data, prefix=""):
        h = "{}_{}_{}".format(prefix, hash(input_text), hash(str(session)))
        file_name = "{}/{}.json".format(self.request_folder, h)
        with open(file_name, 'w') as file:
            json.dump(request_data, file, indent=2)

    def create_request(self, input_text, session=None):
        return SimulationsApiRequest(Input(input_text), Device(self.default_location), None)

    def get_response(self, input_text, session, sb, prefix=""):
        event = self.get_request_event_data(input_text, session, prefix)
        return sb.lambda_handler()(event, event)

    def get_test_response(self, input_text, session, sb, prefix=""):
        event = self.get_request_event_data(input_text, session, prefix)
        lambda_handler = self.create_function_handler(event, sb)
        response = sb.lambda_handler()(event, event)
        return TestResponse(event, lambda_handler, response)

    def get_request_event_data(self, input_text, session, prefix=""):
        data = self.check_if_request_exist(input_text, session, prefix)
        if data != None:
            request_data = data
        else:
            request_data = self.simulate_request(input_text, session).to_dict()
            self.save_request(input_text, session, request_data, prefix)

        try:
            event = request_data['result']['skill_execution_info']['invocation_request']['body']
            if session is not None:
                event['session'] = session
        except Exception as e:
            print(request_data)
            raise e
        return event

    def simulate(self, input_text, session, sb, prefix=""):
        event = self.get_request_event_data(input_text, session, prefix)
        return self.create_function_handler(event, sb)

    def simulate_request(self, input_text, session=None):
        skill_simulation = self.smapi_client.simulate_skill_v1(self.skill_id, self.create_request(input_text, session),
                                                               full_response=True)
        result = None
        for i in range(5):
            time.sleep(1)
            result = self.smapi_client.get_skill_simulation_v1(self.skill_id, skill_simulation.id,
                                                               full_response=True)
            if result.to_dict()['status'] == "SUCCESSFUL":
                break
        if result.to_dict()['status'] != "SUCCESSFUL":
            print("ERROR")
        return result

    def getHandleFunctionName(self, handler_input):
        request_mapper = self.skill.request_dispatcher.request_mappers[0]
        request_handler_chain = request_mapper.get_request_handler_chain(handler_input)
        return request_handler_chain.request_handler.__class__.__name__[14:]

    def create_function_handler(self, event, context=None):
        request_envelope = self.skill.serializer.deserialize(
            payload=json.dumps(event), obj_type=RequestEnvelope)

        if (self.skill.skill_id is not None and
                request_envelope.context.system.application.application_id !=
                self.skill.skill_id):
            raise AskSdkException("Skill ID Verification failed!!")

        if self.skill.api_client is not None:
            api_token = request_envelope.context.system.api_access_token
            api_endpoint = request_envelope.context.system.api_endpoint
            api_configuration = ApiConfiguration(
                serializer=self.skill.serializer, api_client=self.skill.api_client,
                authorization_value=api_token,
                api_endpoint=api_endpoint)
            factory = ServiceClientFactory(api_configuration=api_configuration)
        else:
            factory = None

        template_factory = TemplateFactory(
            template_loaders=self.skill.loaders,
            template_renderer=self.skill.renderer)

        attributes_manager = AttributesManager(
            request_envelope=request_envelope,
            persistence_adapter=self.skill.persistence_adapter)

        handler_input = HandlerInput(
            request_envelope=request_envelope,
            attributes_manager=attributes_manager,
            context=context,
            service_client_factory=factory,
            template_factory=template_factory)
        return handler_input
