import threading
import time
import os

def search_keywords_in_files(file_paths, keywords, results):
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

def threaded_search(file_paths, keywords, num_threads=4):
    threads = []
    results = {}
    files_per_thread = len(file_paths) // num_threads
    
    start_time = time.time()
    
    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = None if i == num_threads - 1 else (i + 1) * files_per_thread
        thread_files = file_paths[start_index:end_index]
        
        thread = threading.Thread(target=search_keywords_in_files, args=(thread_files, keywords, results))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Threading approach took {end_time - start_time:.2f} seconds")
    
    return results

file_paths = ["data/text1.txt", "data/text2.txt", "data/text3.txt", "data/text4.txt"]
keywords = ["in", "coffee", "bakery"]

if __name__ == "__main__":
    results = threaded_search(file_paths, keywords)
    print(results)
