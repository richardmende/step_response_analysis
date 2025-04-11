from numpy import exp


class SystemModel:
    def __init__(self, model_type, order, parameters):
        self.model_type = model_type    # PT or IT
        self.order = order              # 1 / 2 / 3 / 4, dependent on the number of delay time constants of the system
        self.parameters = parameters    # K / T1 / T2 / ...
    

    def step_response(self, t):

        if self.model_type == 'PT':
            response = self.parameters['K']
            for i in range(1, self.order + 1):
                T = self.parameters[f'T{i}']
                response *= (1 - exp(-t / T))
            return response
        
        elif self.model_type == 'IT':
            response = t 
            for i in range(1, self.order + 1):
                T = self.parameters[f'T{i}']
                response *= (1 - exp(-t / T))
            return response
        
        else:
            raise ValueError("Unknown description!")
