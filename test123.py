test_dict = {"c":25, "a":7, "b":10}

if "a" in test_dict.keys():
    test_dict["a"]+=1
else:
    test_dict["c"] = 4

print(sorted(test_dict.values()))
print(test_dict)
print(min(test_dict.values()))
