

import numpy as np


def func(data, a, b, c, d, e, f, g, h):
    diff = [(data[2] - (a/(n[0]*n[1]) + 1 / (b*n[0]+c) + np.exp(-d*abs(e*n[0]+f)+g)+h))**2 for n in data]
    return sum(diff)

if __name__ == '__main__':
    data = 
    params, _ = param_search(func, lambda x: x, 



def param_search(test_func, cost_func, data, n_tests=10, initial_lr=0.01, tolerance=1e-6, precision=1e-4, max_iter=1000, **ranges):
    learning_rate = initial_lr

    parameters = {key: (value[0] + value[1]) / 2 for key, value in ranges.items()}

    delta = {key: (value[1] - value[0]) / n_tests for key, value in ranges.items()}
    
    def clip_param(params):
        return {key: np.clip(val, ranges[key][0], ranges[key][1]) for key, val in params.items()}

    def has_converged(old_params, new_params, precision):
        return all(abs(old_params[key] - new_params[key]) < precision for key in old_params)

    def round_parameters(params, precision):
        return {key: round(val, -int(np.floor(np.log10(precision)))) for key, val in params.items()}

    def validate_parameters(params):
        errors = ''
        for key, value in params.items():
            if not np.isfinite(value) or np.isnan(value):
                errors += f"Invalid parameter detected: {key}={value}\n"
        if errors != '':
            raise ValueError(errors)
    
    test_data = test_func(data, **parameters)
    cost = cost_func(data, test_data)
    itters = 0
    for _ in range(max_iter):
        itters += 1
        gradients = {}
        for key in parameters:
            params_up = parameters.copy()
            params_down = parameters.copy()
            params_up[key] += delta[key]
            params_down[key] -= delta[key]
            params_up = clip_param(params_up)
            params_down = clip_param(params_down)
            cost_up = cost_func(data, test_func(data, **params_up))
            cost_down = cost_func(data, test_func(data, **params_down))
            gradients[key] = (cost_up - cost_down) / (2 * delta[key])
        
        prev_parameters = parameters.copy()
        for key in parameters:
            parameters[key] -= learning_rate * gradients[key]
        parameters = clip_param(parameters)
        validate_parameters(parameters)
        
        if has_converged(prev_parameters, parameters, precision):
            print("Converged based on parameter precision.")
            break
        
        new_test_data = test_func(data, **parameters)
        new_cost = cost_func(data, new_test_data)
        
        if abs(new_cost - cost) < tolerance:
            print("Converged based on cost tolerance.")
            break
        
        if new_cost > cost:
            learning_rate /= 2  # Reduce learning rate if cost increases
            parameters = prev_parameters  # Revert to previous parameters
        else:
            learning_rate *= 1.05  # Slightly increase learning rate if cost decreases
        
        cost = new_cost

    print(itters)
    parameters = round_parameters(parameters, precision)
    final_reduced_data = test_func(data, **parameters)
    return parameters, final_reduced_data

