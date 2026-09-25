import os
import requests
import json

screens_data = [
    {
        "id": "b1ab50bf35e045e49351eb0792417fa2",
        "title": "Landing_Page",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjg0ODY0ZmMwOTM0ZjM4ZjY4MTc1MzI2EgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1UqszHwxa_0ocpBqohYCYL7x6C_y7xBHWXnNvLdyD7CEsIC2tXRa-nkIv9tKgYohCxaggMIGrRQgpGzn_LRE6yfcfuyGJnwPRZBWvZ4gvrt_3co8DoEsuBDgAljNzKGSx8_oUmMQ8aL0sKLNSitKjJXd4F3MLXsqfOF7gf03ACx9rOxOdDC5kNQuwTWhpM9RZgzAqEwCOpzYVEjsEyfAIu3WrAfT4cipnpUA12s_l3_Pz8aToPjZDZy1fG_"
    },
    {
        "id": "b81aca6240734144adf42c42fcd15994",
        "title": "Data_Morphing",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjllNWM5ODgwOTEwNzZmOTU3MDRhN2RjEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1WhVK0Jr8M0oOQIDxJhLGJwIatKypCca3yWQcQhBjSKoqPNyOJ_Ma5omnxSGQAnjKuuKBvHBszRLl9T_nbEK9oaYTPcO9F3BajlegFrR16cK6S1-4K0ciZLvRBuihWdGG-L10ux9B3VkQmaXvVlC2VPU4Wmt_Mvw-uEDEFylb_FppMPNbUONJW0prrRzgLMzTUM52Y3_-Ll6hf6GjsJ_CE5WkHzbfMViKis2Rw9SkHYzWj1N7Xzhxoy2WJd"
    },
    {
        "id": "1f259cc32b8845c8a8a8689b566be04b",
        "title": "Visualization_Studio",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjk3Yjk1NjAwNDczNmMxNDRkMTI4YTcwEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1UkglvxyVNsybLafnq0gob_963T_-7Ne1bw973qvFmCBmPb1lri5jYobzEMwhSaBM4tarBX5mc-QbC_AbqsRwipaxsnSDNz3QZqHK_iFNxM3iesCI0H9H0YH-WWVN0KRLkxDqfJukkgPS-zyrZmZcy-gprLeqTLT3C25EeplC0HsftcZOyR3v-8keNO_gb5ZazGi5rZB1TvWVNaORzNZHGc5BPbDhpmKNt_Ritmihs0ldBZAkCtEkxTQbA"
    },
    {
        "id": "9b80561ed8cb43909cf4d1a79f3e3f07",
        "title": "Shader",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjU4YzVkYjgwOTM0ZjM4ZjY4MTc1MzI2EgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": None
    },
    {
        "id": "e8100cb060a74cdd9cf9001b16e6bf7c",
        "title": "Export_Ready",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjkyZGJiMDYwNzc5ODRmNGMxMmM0NjA4EgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1W8w8L9i9DBFXkbAInGXSJDQYN9lBrfxOp0-R6Z0fpzmbi3Mm0AIvCDmjzKXwSZ5CLpKPeHO0Vxu8wQkwF6F9kTZY55wa35Jiq3MW-qedumwnWgS9_ksiwkaXE5osrTS3FQs8XoQCJvstvrRpWykGZFq82GReAjKxZOlLc-gTYzk2EAt4zxjPrSS2vvtNYUKgMMvr-9uJOuiAR0CESQ1lGLEi5nzLh_73jDZ38xEyVdz8i2pFOuZ5cUcIT6"
    },
    {
        "id": "c1c6cbc085ea496eb3b22cd82ae4ecd5",
        "title": "Ask_Your_Data",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjg3NTZkNzYwMzM4NWVlNTgzMDIzNWUwEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1XKoixdAeJXskMvugbJ9YbkYXoIfmHzvtz6-pmjYq94dBSwF_fDAlzIoFnGOXn1vpGW0eE4IE_sULSVCL7I8Peyxgtfm_g_AM68WYJas2ehpMHiRM61e7bfkJdjgTCt2nY0XZcrKUsgaKh4NJiulyTVxJoLaLZMeXxRwJwG1MKMyUENXmnAqNFh5NlophR5Fsl7qWAUxsRG--SrRsbDKDNGrspoFIbcwehqQZELFdFNx432uaGOMC4llopq"
    },
    {
        "id": "a517ece57e9841389a07a47ea8c0fc80",
        "title": "Report_Builder",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjk5NDYzMjQwMWI0ZTQ0Yzg5MzUzYzI0EgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1VgtyiWmy0CPatGUfLgwNyWFVBtGbTBUKCyIiH0ZmvtHOZkCJr6NRa_l4_2F-JnJ3u4RUjAPejWNlMij02RIVS1g3pjOMlWNUMG_ZC2qFDh8-rvT3WvxtdzjUkG69PkIXB9nE7DW_3I8pWjvt46w4lL6MJswTz9GnceWQXwPO3alOeK-rgzWKrrooAx6wTUX5es-uT2k9qyM2p9O1HJiJbT0mVl6gzOLyItpuBsyTL4ioNflNsy5xZnGpQ"
    },
    {
        "id": "4310f098d7964dea852af01eddaaa349",
        "title": "Three_JS",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjU5NGNiMmMwNzNhZDYwYmIxMmMyZjVlEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": None
    },
    {
        "id": "3fc695a5f3b140c9a18d42a05d8f7e11",
        "title": "Workspace_Upload",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjg4OTc2MTkwMmE5YjNlY2RhMjc3ZTMzEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1XsEOznpouUlN82aHRAaFktB6Wz517W1_OJNLGO8n08192PEOiVBsz8YvE0Q9SPtXDxelqAuUU6w2SCCOLvoVfVk2a7ayfO3arC4VGH2jImZffdRBlL4n4y48A_Nz94YGh7ege09SYgCNUzKjsBmeA5-BQ47wvJoTep47v24iAVUBbqPyGmyxjgMojfPrLvjOZSazuuNfvAkPSzi_kzU1B-2p4t0q_h9TPOM8rWb03eLom-4CEHPKh9xGuU"
    },
    {
        "id": "26f3ca1db17d4088900024714680dff3",
        "title": "AI_Understanding",
        "html_url": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1YTQzYjhmZDkyNjgwNjM5NDg5NzE0MDJjMTFkEgsSBxCK9tb-vBIYAZIBJAoKcHJvamVjdF9pZBIWQhQxODQxOTcwNjI3OTExMDQyMDc2Ng&filename=&opi=89354086",
        "img_url": "https://lh3.googleusercontent.com/aida/AEtjO1XKGDM_kBQricAqxUha30IWkg_9zC9BNKrKbGdN_V2nURYr7k4daGxw0BYk5h67Gj9l8NmkgHwkna9AOgEmKihqTEaLxl12vII0zWZkntbv7Yi3H2wQxQHxKuKrqrJCL31sC7B9PZzIJOheeaainjEbYT-KCZzJnWuE6mA8M5_HVW2NLvZ1goYeSoxdj6--wKKPHBm1Idm4Vi1gK3d1zcs0-V6AWgs70JWmJi8PwArdznUAII_JSzUA_lc-"
    }
]

out_dir = os.path.join(os.path.dirname(__file__), "..", "stitch_screens")
os.makedirs(out_dir, exist_ok=True)

for sc in screens_data:
    print(f"Downloading screen: {sc['title']} ({sc['id']})...")
    # Download HTML
    if sc.get("html_url"):
        try:
            r = requests.get(sc["html_url"], timeout=30)
            if r.status_code == 200:
                html_path = os.path.join(out_dir, f"{sc['title']}_{sc['id']}.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"  -> Saved HTML: {html_path}")
        except Exception as e:
            print(f"  Error downloading HTML: {e}")

    # Download image
    if sc.get("img_url"):
        try:
            r = requests.get(sc["img_url"], timeout=30)
            if r.status_code == 200:
                img_path = os.path.join(out_dir, f"{sc['title']}_{sc['id']}.png")
                with open(img_path, "wb") as f:
                    f.write(r.content)
                print(f"  -> Saved Screenshot: {img_path}")
        except Exception as e:
            print(f"  Error downloading Image: {e}")

print("All Stitch assets downloaded successfully!")
