""" M/M/1 queue model

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-08-07
:Copyright: 2020, Karr Lab
:License: MIT
"""

import numpy

import de_sim


class CustomerArrives(de_sim.EventMessage):
    "A customer arrives at the queueing system"


class ServiceEnds(de_sim.EventMessage):
    "A customer's service ends, and they depart the queueing system"


MESSAGE_TYPES = [CustomerArrives, ServiceEnds]


class MM1SimulationObject(de_sim.SimulationObject):  # pragma no cover; unit test not written yet
    """ M/M/1 queue """

    def __init__(self, name, lambda_, mu):
        super().__init__(name)
        self.lambda_ = lambda_
        self.mu = mu
        self.queue_len = 0
        self.busy = False
        self.queue_len_history = [(0., 0)]
        self.random_generator = numpy.random.default_rng()

    def schedule_next_arrival(self):
        self.send_event(self.random_generator.exponential(1./self.lambda_), self, CustomerArrives())

    def schedule_service_end(self):
        self.busy = True
        self.send_event(self.random_generator.exponential(1./self.mu), self, ServiceEnds())

    def init_before_run(self):
        self.schedule_next_arrival()

    def add_to_queue(self):
        self.queue_len += 1
        self.queue_len_history.append((self.time, self.queue_len))

    def remove_from_queue(self):
        self.queue_len -= 1
        self.queue_len_history.append((self.time, self.queue_len))

    def handle_customer_arrives(self, event):
        self.schedule_next_arrival()
        if self.busy:
            self.add_to_queue()
        else:
            self.schedule_service_end()

    def handle_service_ends(self, event):
        self.busy = False
        if self.queue_len:
            self.remove_from_queue()
            self.schedule_service_end()
        
    event_handlers = [(CustomerArrives, 'handle_customer_arrives'),
                      (ServiceEnds, 'handle_service_ends')]

    # register the message types sent
    messages_sent = MESSAGE_TYPES


def run_MM1_simulation(max_time, lambda_, mu):  # pragma no cover; unit test not written yet
    MM1_sim_obj = MM1SimulationObject('MM1_sim_obj', lambda_, mu)
    simulator = de_sim.Simulator()
    simulator.add_object(MM1_sim_obj)

    # run the simulation
    simulator.initialize()
    simulator.run(max_time)

    # print queue len history
    print("time\tqueue len")
    for time, queue_len in MM1_sim_obj.queue_len_history:
        print(f"{time:.2f}\t{queue_len:>6}")


run_MM1_simulation(10, 3, 5)