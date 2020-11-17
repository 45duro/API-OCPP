id_tag = "miTagId9999",
connector_id = 12,
charging_profile = {
    "charging_profile_id" : 20,
    "stack_level" : 90, 
    "charging_profile_purpose":"ChargePointMaxProfile",
    "charging_profile_kind" :"Absolute",
    "charging_schedule": {
        "charging_rate_unit":"W",
        "charging_schedule_period": [
            {"start_period": 20},
            {"limit": 0.9}
        ]
    }   
    
}

x = charging_profile["charging_schedule"]
y = x["charging_schedule_period"]
print (y)
print(type(y))