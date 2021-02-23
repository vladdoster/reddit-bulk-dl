# Reddit Bulk Downloader

Downloads Reddit media
  

## [Download the latest release here](https://github.com/aliparlakci/bulk-downloader-for-reddit/releases/latest)

## Usage
If you run **Windows**, after you extract the zip file, double-click on the *bulk-downloader-for-reddit.exe*. The program will guide you through. Also, take a look at the [Setting up the program](#🔨-setting-up-the-program) section. **However**, Bulk Dowloader for Reddit has a plenty of features which can only be activated via command line arguments. See [Options](#⚙-Options) for it.

Unfortunately, there is no binary for **MacOS** or **Linux**. If you are a MacOS or Linux user, you must use the program from the source code. See the [Interpret from source code](docs/INTERPRET_FROM_SOURCE.md) page.
  
However, binary version for Linux is being worked. So, stay tuned.
  
OR, regardless of your operating system, you can fire up the program from the **source code**.

### `python3 -m pip install -r requirements.txt`

### `python3 script.py`

See the [Interpret from source code](docs/INTERPRET_FROM_SOURCE.md) page for more information.

## 🔨 Setting up the program
### 📽 ffmpeg Library
  
Program needs **ffmpeg software** to add audio to some video files. However, installing it is **voluntary**. Although the program can still run with no errors without the ffmpeg library, some video files might have no sound.
  
Install it through a package manager such as **Chocolatey** in Windows, **apt** in Linux or **Homebrew** in MacOS:

- **in Windows**: After you **[install Chocolatey](https://chocolatey.org/install)**, type **`choco install ffmpeg`** in either Command Promt or Powershell.
- **in Linux**: Type **`sudo apt install ffmpeg`** in Terminal.
- **in MacOS**: After you **[install Homebrew](https://brew.sh/)**, type **`brew install ffmpeg`** in Terminal

OR, [Download ffmpeg](https://www.ffmpeg.org/download.html) manually on your system and [add the bin folder in the downloaded folder's dir to `PATH` of your system.](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) However, package manager option is suggested.

## 🐋 Docker
There is also a complete ready to go Docker integration. Install **Docker** and **docker-compose**. Then run the following command from the repository root:
### `docker-compose run --service-ports bdfr`
And you'll find youself right in the app. The files will be downloaded to `downloads/`. Since it is docker, you may want to change the ownership of the files once you're done (belongs to root by default).

_Credits to [wAuner](https://github.com/wAuner)_

## ⚙ Options

Some of the below features are available only through command-line.
  
Open the [Command Promt](https://youtu.be/bgSSJQolR0E?t=18), [Powershell](https://youtu.be/bgSSJQolR0E?t=18) or [Terminal](https://youtu.be/Pz4yHAB3G8w?t=31) in the folder that contains bulk-downloader-for-reddit file (click on the links to see how)
  
After you type **`bulk-downloader-for-reddit.exe`**, type the preffered options.

Example: **`bulk-downloader-for-reddit.exe --subreddit pics --sort top --limit 10`**

## **`--subreddit`** 
Downloads posts from given subreddit(s). Takes number of subreddit names as a paramater.
  
Example usage: **`--subreddit IAmA pics --sort hot --limit 10`**

## **`--multireddit`**
Downloads posts from given subreddit. Takes a single multireddit name as a parameter. **`--user`** option is required.
  
Example usage: **`--multireddit myMulti --user me --sort top --time week`**

## **`--search`**
Searches for given query in given subreddit(s) or multireddit. Takes a search query as a parameter. **`--subreddit`** or **`--multireddit`** option is required. **`--sort`** option is required.
  
Example usage: **`--search carter --subreddit funny`**
  
## **`--submitted`** 
Downloads given redditor's submitted posts. Does not take any parameter. **`--user`** option is required.

Example usage: **`--submitted --user spɛz --sort top --time week`**
  
## **`--upvoted`**
Downloads given redditor's upvoted posts. Does not take any parameter. **`--user`** option is required.

Example usage: **`--upvoted --user spɛz`**
  
## **`--saved`** 
Downloads logged in redditor's saved posts. Does not take any parameter. Example usage: **`--saved`**
  
## **`--link`**
Takes a reddit link as a parameter and downloads the posts in the link. Put the link in " " (double quotes).
  
Example usage: **`--link "https://www.reddit.com/r/funny/comments/25blmh/"`**

## **`--log`**
Program saves the found posts into POSTS.json file and the failed posts to FAILED.json file in LOG_FILES folder. You can use those files to redownload the posts inside them.  
  
Uses a .json file to redownload posts from. Takes single dir to a .json file as a parameter.

Example usage: **`--log D:\pics\LOG_FILES\FAILED.json`**

---

## **`--user`**
Takes a reddit username as a parameter. Example usage: **`--user spɛz`**
  
## **`--sort`**
Takes a valid sorting type as a parameter. Valid sort types are `hot`, `top`, `new`, `rising`, `controversial` and `relevance` (if you are using `--search` option)

Example usage: **`--sort top`**
  
## **`--time`**
Takes a valid time as a parameter. Valid times are `hour`, `day`, `week`, `month`, `year` and `all`. Example usage: **`--time all`**
  
## **`--limit`**
Takes a number to specify how many should program get. Upper bound is 1000 posts for **each** subreddit. For example, if you are downloading posts from pics and IAmA, the upper bound is 2000. Do not use the option to set it to highest bound possible.

Example usage: **`--limit 500`**

---

## **`--skip`**
Takes a number of file types as a parameter to skip the posts from those domains. Valid file types are `images`, `videos`, `gifs`, `self`
  
Example usage: **`--skip self videos`**
  
## **`--skip-domain`**
Takes a number of domains as a parameter to skip the posts from those domains.

Example usage: **`--skip v.redd.it youtube.com youtu.be`**
  
## **`--quit`**
Automatically quits the application after it finishes. Otherwise, it will wait for an input to quit.

Example usage: **`--quit`**
  
## **`--dir`**
Takes a dir which the posts should be downloaded to. Overrides the given default dir. Use `..\` to imply upper level and `.\` to imply the current level.

Example usage: **`--dir D:\bdfr\`**  
Example usage: **`--dir ..\images\`**  
Example usage: **`-d ..\images\`**  
Example usage: **`-d .\`**  
  
## **`--set-f_name`**
Starts the program to set a f_name template to use for downloading posts. **Does not take any parameter.**
  
When the programs starts, you will be prompted to type a f_name template. Use `SUBREDDIT`, `REDDITOR`, `POSTID`, `TITLE`, `UPVOTES`, `FLAIR`, `DATE` in curly brakets `{ }` to refer to the corrosponding property of a post.

❗ Do NOT change the f_name structure frequently. If you did, the program could not find duplicates and would download the already downloaded files again. This would not create any duplicates in the dir but the program would not be as snappy as it should be.
  
The default f_name template is **`{REDDITOR}_{TITLE}_{POSTID}`**

Example usage: **`--set-f_name`**
  
## **`--set-folderpath`**
Starts the program to set a folder structure  to use for downloading posts. **Does not take any parameter.**
  
When the programs starts, you will be prompted to type a f_name template. Use `SUBREDDIT`, `REDDITOR`, `POSTID`, `TITLE`, `UPVOTES`, `FLAIR`, `DATE` in curly brakets `{ }` to refer to the corrosponding property of a post. Do not put slashes `/` or backslashes `\` at either ends. For instance, **`{REDDITOR}/{SUBREDDIT}/{FLAIR}`**
  
The default f_name template is **`{SUBREDDIT}`**

Example usage: **`--set-folderpath`**
  
## **`--set-default-dir`**
Starts the program to set a default dir to use in case no dir is given. **Does not take any parameter.**
  
When the programs starts, you will be prompted to type a default dir. You can use {time} in foler names to use to timestamp it. For instance, **`D:\bdfr\posts_{time}`**

Example usage: **`--set-default-dir`**
  
## **`--use-local-config`**
Sets the program to use config.json file in the current dir. Creates it if it does not exists. Useful for having different configurations. **Does not take any parameter.**
  
Example usage: **`--use-local-config`**
  
## **`--no-dupes`**
Skips the same posts in different subreddits. Does not take any parameter.

Example usage: **`--no-dupes`**
  
## **`--no-download`**
Quits the program without downloading the posts. Does not take any parameter

Example usage: **`--no-download`**
  
## **`--downloaded-posts`**
Takes a file dir as a parameter and skips the posts if it matches with the post IDs inside the file. It also saves the newly downloaded posts to the given file.

Example usage: **`--downloaded-posts D:\bdfr\ALL_POSTS.txt`**
  
## ❔ FAQ

### I am running the script on a headless machine or on a remote server. How can I authenticate my reddit account?
- Download the script on your everday computer and run it for once.
- Authenticate the program on both reddit and imgur.
- Go to your Home folder (for Windows users it is `C:\Users\[USERNAME]\`, for Linux users it is `/home/[USERNAME]`)
- Copy the *config.json* file inside the Bulk Downloader for Reddit folder and paste it **next to** the file that you run the program.

### How can I change my credentials?
- All of the user data is held in **config.json** file which is in a folder named "Bulk Downloader for Reddit" in your **Home** dir. You can edit them, there.  

  Also if you already have a config.json file, you can paste it **next to** the script and override the one on your Home dir. 

### What do the dots resemble when getting posts?
- Each dot means that 100 posts are scanned.

### Getting posts takes too long.
- You can press *Ctrl+C* to interrupt it and start downloading.

### How do I open self post files?
- Self posts are held at reddit as styled with markdown. So, the script downloads them as they are in order not to lose their stylings.
  However, there is a [great Chrome extension](https://chrome.google.com/webstore/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk) for viewing Markdown files with its styling. Install it and open the files with [Chrome](https://www.google.com/intl/tr/chrome/).  

  However, they are basically text files. You can also view them with any text editor such as Notepad on Windows, gedit on Linux or Text Editor on MacOS.
