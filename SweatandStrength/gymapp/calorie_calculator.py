def calculate_calorie_intake(weight_kg, height_cm, age, gender):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Gender should be 'male' or 'female'")

    # Applying activity factor (sedentary to very active)
    activity_factor = {'sedentary': 1.2, 'lightly active': 1.375, 'moderately active': 1.55, 'very active': 1.725}
    total_calories = bmr * activity_factor['moderately active']  # Change activity level here

    return total_calories