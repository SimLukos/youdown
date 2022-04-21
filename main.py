from pytube import YouTube


def video_Parsiuntimas(link):
    video = YouTube(link)
    video = video.streams.get_highest_resolution()
    video.download()

def video_Pavadinimas(link):
    video = YouTube(link)
    pavadinimas = video.title
    return pavadinimas

def video_Perziuros(link):
    video = YouTube(link)
    perziuros = video.views
    return perziuros

def video_Autorius(link):
    video = YouTube(link)
    autorius = video.author
    return autorius

link = 'https://www.youtube.com/watch?v=7BXJIjfJCsA'
print(video_Pavadinimas(link))