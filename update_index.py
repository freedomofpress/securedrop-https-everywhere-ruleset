import os


def update_index(target_file='index.html',
                 dir_to_serve='channel'):
    html_content = "<html>"
    files = os.listdir(dir_to_serve)
    for file_ in files:
        html_content += "<a href='{dir}/{file}'>{file}</a><br> ".format(
            dir=dir_to_serve, file=file_)
    html_content += "</html>"

    with open(target_file, "w") as f:
        f.write(html_content)


if __name__=='__main__':
    update_index()
