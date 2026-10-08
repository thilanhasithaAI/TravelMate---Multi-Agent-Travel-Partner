from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


# test the tavily search function

# response = tavily_search("what are the best hotels in Sri lanka")
# print(response)

# test the search flights function

results = search_flights("Plan a 7 days Japan trip from sri lanka including flights and hotels")
print(results)


