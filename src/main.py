from json_parser import JsonParser
import time

def main():
    parser = JsonParser()
    parser.extract_from_json()
    parser.generate_graphs()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
