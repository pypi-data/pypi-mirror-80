from swap.api.clients import UBLClient
from swap.api.models import WorkflowServiceChain, CommandInput
from swap.api.sequences.builders import DefaultCommandSequenceBuilder
from swap.common.logging import logger


class Workflow:
    def __init__(self):
        self.service_chain_uuid = None
        self.service_chains = {}
        self.ubl_client = UBLClient()
        self.command_sequence = DefaultCommandSequenceBuilder().build()

    def create_service_chain(self, name):
        self.service_chains[name] = WorkflowServiceChain(datasets=[], services=[])

    def submit(self, wait=False):
        output = {}
        for key, service_chain in self.service_chains.items():
            command_input = CommandInput(response=None, service_chain=service_chain, wait=wait)
            output[key] = self.command_sequence.call(command_input)
            return output if not wait else \
                logger.info(f"Workflow submit set to wait={wait}. "
                f"Execution Request sent for Service Chain UUID: {command_input.response['Execution_sent']}. "
                f"Call Workflow.status() for status updates.")

    def service_chain(self, name):
        return self.service_chains[name]

    def status(self):
        output = {}
        for key, service_chain in self.service_chains.items():
            command_input = CommandInput(response=None, service_chain=service_chain, wait=True)
            output[key] = self.command_sequence.call(command_input)

        return output

