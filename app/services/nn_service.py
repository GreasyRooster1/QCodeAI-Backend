def calculate_forward_pass(inputs: list[float], layers: list[dict]) -> dict:
    simulation_history = {
        "initial_inputs": inputs,
        "layer_outputs": []
    }
    
    current_activations = inputs
    
    for layer in layers:
        next_activations = []
        
        for i, node_weights in enumerate(layer["weights"]):
            node_sum = layer["biases"][i]
            
            for j, weight in enumerate(node_weights):
                node_sum += current_activations[j] * weight
            
            final_activation = max(0.0, node_sum)
            next_activations.append(final_activation)
            
        simulation_history["layer_outputs"].append(next_activations)
        current_activations = next_activations
    
    return simulation_history