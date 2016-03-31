import os


# Each project should have its own directory
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory {}'.format(directory))
        os.makedirs(directory)


# Create queue and crawled files for links (if not created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    video_links = project_name + '/video_urls.txt'
    video_player_links = project_name + '/video_player_urls.txt'
    crawled_video_player_links = project_name + '/crawled_video_player_urls.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(video_links):
        write_file(video_links, '')
    if not os.path.isfile(video_player_links):
        write_file(video_player_links, '')
    if not os.path.isfile(crawled_video_player_links):
        write_file(crawled_video_player_links, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data + '\n')


# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a', encoding='utf-8') as file:
        file.write(data + '\n')


# Delete the contents of a file
def delete_file_contents(path):
    with open(path, 'w', encoding='utf-8'):
        pass


# Read a file and convert each file line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt', encoding='utf-8') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Iterate through a set, each item will be a lien in a file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)
