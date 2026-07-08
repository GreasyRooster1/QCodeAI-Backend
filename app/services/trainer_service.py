import random

def pet_evo(reward_speed: float, reward_neatness: float, generations: int) -> dict:
    pet_speed = 0.5
    pet_neatness = 5.0
    history = []
    
    for gen in range(1, generations + 1):
        mutations = []
        for _ in range(5):
            mut_speed = max(0.0, min(10.0, pet_speed + random.uniform(-2.0, 2.0)))
            mut_neatness = max(0.0, min(10.0, pet_neatness + random.uniform(-2.0, 2.0)))
            
            fitness_score = (mut_speed * reward_speed) + (mut_neatness * reward_neatness)
            
            mutations.append({
                "speed": mut_speed,
                "neatness": mut_neatness,
                "score": fitness_score
            })
        
        mutations.sort(key=lambda x: x['score'], reverse=True)
        best_pet = mutations[0]
        
        pet_speed = best_pet['speed']
        pet_neatness = best_pet['neatness']
        
        if pet_speed > 8.0 and pet_neatness < 4.0:
            behavior = "Zoomed around the room, shoved all the toys under the rug to finish faster!"
        elif pet_neatness > 8.0 and pet_speed < 4.0:
            behavior = "Carefully placed one toy perfectly in the box. Took 3 hours."
        elif pet_speed > 7.0 and pet_neatness > 7.0:
            behavior = "The perfect AI pet! Cleaned the room quickly and spotless."
        elif pet_speed < 4.0 and pet_neatness < 4.0:
            behavior = "Sat down, got confused, and chewed on a shoe. Didn't clean."
        else:
            behavior = "Did an okay job cleaning, moving at a normal pace."
            
        history.append({
            "generation": gen,
            "speed_stat": round(pet_speed, 1),
            "neatness_stat": round(pet_neatness, 1),
            "fitness_score": round(best_pet['score'], 1),
            "behavior": behavior
        })
        
        history.sort(key=lambda x: x["fitness_score"], reverse=True)
    
    return {"history": history}