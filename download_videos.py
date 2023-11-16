import requests
import os
import json

def clean_videos_folder():
    os.system("rm videos/*")

def download_videos():
    URL = "https://www.reddit.com/r/oddlysatisfying/top.json?sort=top&t=day&limit=10"
    res = requests.get(URL, headers={'User-agent': 'reddit scrapper'})
    json_res = res.json()
    manifest_json = {"data": []}

    for idx in range(10):
        try:
            submission_data = json_res['data']['children'][idx]['data']
            if submission_data['is_video'] == False:
                continue
            if submission_data['secure_media'] == None:
                continue
            if submission_data['secure_media']['reddit_video'] == None:
                continue
            if submission_data['secure_media']['reddit_video']['fallback_url'] == None:
                continue
            if submission_data['secure_media']['reddit_video']['duration'] == None:
                continue

            fallback_url = submission_data['secure_media']['reddit_video']['fallback_url']
            title = submission_data['title']

            r = requests.get(fallback_url, stream=True)
            formatted_title = title.replace(' ', '_').replace('(', '').replace(')', '').lower()
            with open(f"videos/{formatted_title}.mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)

            filename = f"{formatted_title}.mp4"
            new_file_name = f"output.{filename}"
            os.system(f"ffmpeg -i videos/{filename} videos/{new_file_name}")
            os.system(f"rm videos/{filename}")

            manifest_json["data"].append({
                "filename": filename,
                "title": title,
            })
        except Exception as e:
            print(idx)

    with open("videos/manifest.json", "w") as f:
        json.dump(manifest_json, f)

def main():
    clean_videos_folder()
    download_videos()

if __name__ == '__main__':
    main()