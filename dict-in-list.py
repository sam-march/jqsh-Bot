list = []
dict = {}

while True:
  member = input("Please input member id: ")
  warn_id = input("Please input warn id: ")
  warn_reason = input("Please input warn reason: ")
  
  dict["member"] = member
  dict["warn_id"] = warn_id
  dict["warn_reason"] = warn_reason
  
  list.append(dict)
  print(list)
