from github import Github, Auth

def check_for_updates():
    github_token = "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"
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    repo = g.get_user().get_repo("TaskReminder")
    conts = repo.get_releases()
    latest = conts.get_page(0).__getitem__(0).get_assets().get_page(0)[0]
    link = latest.browser_download_url
    version = latest.name
    _ver = version.find('1')
    version = version[_ver:_ver+5]

    g.close()

    return link, version