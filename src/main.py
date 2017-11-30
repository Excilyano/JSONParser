from json_parser import JsonParser
import time

def main():

    start_time = time.time()

    parser = JsonParser()
    parser.extract_from_json()
    parser.generate_graphs()

    print("TOTAL EXECUTION TIME --- %s seconds ---\n\n" % (time.time() - start_time))

    print("TOTAL SQL PARSING TIME (Mock using Object representation) --- %s seconds ---\n" % (parser.sql_parsing_duration))
    print("TOTAL JSON PARSING TIME --- %s seconds ---\n" % (parser.json_parsing_duration))
    print("TOTAL GRAPH GENERATION TIME --- %s seconds ---\n" % (parser.graph_generation_duration))        

if __name__ == "__main__":
    main()
 
