import torch
from torch import nn
from archi_hard_batch.interface import Interface
from archi_hard_batch.controller import Controller
from archi_hard_batch.memory import Memory
import archi_hard_batch.param as param


class Computer(nn.Module):

    def __init__(self):
        super(Computer, self).__init__()
        self.memory=Memory()
        self.controller=Controller()
        self.interface=Interface()
        self.last_read_vector=torch.Tensor(param.W, param.R)

    def forward(self, input):
        input_x_t=input.cat(self.last_read_vector.view(-1))
        output, interface=self.controller(input_x_t)
        interface_output_tuple=self.interface(interface)
        self.last_read_vector=self.memory(interface_output_tuple)
        return output

    def reset_parameters(self):
        self.memory.reset_parameters()
        self.controller.reset_parameters()
        self.last_read_vector.zero_()
        # no parameter in interface

    def new_sequence_reset(self):
        # I have not found a reference to this function, but I think it's reasonable
        # to reset the values that depends on a particular sequence.
        self.controller.new_sequence_reset()
        self.last_read_vector.zero_()


if __name__=="__main__":

    story_limit=150
    epoch_batches_count=1000
    epochs_count=100
    lr=1e-5
    computer=Computer()
    computer=computer.cuda()

    optimizer=torch.optim.Adam(computer.parameters(),lr=lr)

    train(computer,optimizer,story_limit, batch_size)