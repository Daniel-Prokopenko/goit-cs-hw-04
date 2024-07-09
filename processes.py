import multiprocessing
import time
import os

def search_keywords_in_files(file_paths, keywords, queue):
    results = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in results:
                            results[keyword] = []
                        results[keyword].append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    queue.put(results)

def multiprocessing_search(file_paths, keywords, num_processes=4):
    processes = []
    queue = multiprocessing.Queue()
    files_per_process = len(file_paths) // num_processes
    
    start_time = time.time()
    
    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = None if i == num_processes - 1 else (i + 1) * files_per_process
        process_files = file_paths[start_index:end_index]
        
        process = multiprocessing.Process(target=search_keywords_in_files, args=(process_files, keywords, queue))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"Multiprocessing approach took {end_time - start_time:.2f} seconds")
    
    results = {}
    while not queue.empty():
        partial_results = queue.get()
        for keyword, paths in partial_results.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(paths)
    
    return results

file_paths = ["data/text1.txt", "data/text2.txt", "data/text3.txt", "data/text4.txt"]
keywords = ["in", "coffee", "bakery"]

if __name__ == "__main__":
    results = multiprocessing_search(file_paths, keywords)
    print(results)
