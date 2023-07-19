#Calculations 
def calculate_projection(request):
    current_balance = request["balance"]
    charge_balance = 0

    for i in range (1, request["years"]):
        current_balance = current_balance * (1 + request["growthRate"] / 100)
        for charge_tier in request["charges"]:
            if current_balance >= charge_tier["min"] and current_balance <= charge_tier["max"]:
                charge_balance += (current_balance * (charge_tier["charge_rates"] / 100) + charge_tier["Charge_flat"])
                current_balance -= (current_balance * (charge_tier["charge_rates"] / 100) + charge_tier["Charge_flat"])

    return {    "Final_balance": "{:.2f}".format(current_balance),
                "Balance_of_charges": "{:.2f}".format(charge_balance) }  

def calculate_withRIY(request):
    response = calculate_projection(request)

    currentGrowth = request["growthRate"]
    newEndBalance = response["Final_balance"]
    riyRequest = {  "balance": request["balance"],
                    "growthRate": request["growthRate"], 
                    "years": request["years"], 
                    "charges": [] }

    while newEndBalance >= response["Final_balance"] and currentGrowth > 0:
        currentGrowth -= 0.1
        riyRequest["growthRate"] = currentGrowth
        newEndBalance = calculate_projection(riyRequest)["Final_balance"]

    return {    "Final_balance": response["Final_balance"], 
                "Balance_of_charges": response["Balance_of_charges"], 
                "Riy": "{:.2f}".format(request["growthRate"] - currentGrowth)}  
    
#Main code 
result = calculate_withRIY({    "balance": 100000, 
                                "growthRate": 5, 
                                "years":10,
                                "charges": [{ "min": 1,      "max" : 200000,          "charge_rates": 2, "Charge_flat": 0 },
                                            { "min": 200001, "max": 1000000000000000, "charge_rates": 1, "Charge_flat": 0 },
                                            { "min": 1 ,     "max": 1000000000000000, "charge_rates": 0, "Charge_flat": 500 }] })
print("Final balance : £", result["Final_balance"])
print("Final charges taken : £", result["Balance_of_charges"])
print("RIY : ", result["Riy"])

#result = calculate_projection({"balance": 100000, "growthRate": 2.9, "years":40,
#                                "charges": []})
#print("Final balance : £", result["Final_balance"])
#print("Final charges taken : £", result["Balance_of_charges"])

#Hello its adam :)
#2+2=4"
# This was kelly
#Jude was here
