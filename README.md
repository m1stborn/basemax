<div id="top"></div>

[//]: # ([![Contributors][contributors-shield]][contributors-url])
[//]: # ([![Forks][forks-shield]][forks-url])
[//]: # ([![Stargazers][stars-shield]][stars-url])
[//]: # ([![MIT License][license-shield]][license-url])
[//]: # ([![LinkedIn][linkedin-shield]][linkedin-url])

![Python][python-shield]
![LINE][line-shield]

[//]: # ([![Tests]&#40;https://github.com/m1stborn/CPBL-Linebot/actions/workflows/default-test.yml/badge.svg&#41;]&#40;https://github.com/m1stborn/CPBL-Linebot/actions/workflows/default-test.yml&#41;)

[//]: # (![Flask][flask-shield])
[//]: # ([![Build Status]&#40;https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fm1sborn%2FCPBL-Linebot%2Fbadge%3Ftoken%3D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&style=for-the-badge&label=Tests&#41;]&#40;https://actions-badge.atrox.dev/m1sborn/CPBL-Linebot/goto?token=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&#41;)
[//]: # ([![Build Status]&#40;https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fm1stborn%2FCPBL-Linebot%2Fbadge&style=for-the-badge&label=Tests&#41;]&#40;https://actions-badge.atrox.dev/m1stborn/CPBL-Linebot/goto&#41;)
[//]: # ([![Issues][issues-shield]][issues-url])



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/m1stborn/CPBL-Linebot">
    <img src="assets/550-5508061_baseball-player-vector-clipart.png" alt="Logo" width="80" height="90">
  </a>

<h3 align="center">BaseMax</h3>

  <p align="center">
    LINE聊天機器人: 透過LINE獲得<b>中華職棒</b>即時文字轉播以及數據查詢等功能，加入好友即可開始使用!<br />
    A LINE chatbot provide <b>CPBL Baseball</b> game stats and live broadcast.  
    <br />
    <a href="https://lin.ee/VhvKZLS"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/zh-Hant.png" alt="加入好友" height="36" border="0"></a>
    <br />
    <img src="https://qr-official.line.me/sid/M/591tovcw.png?shortenUrl=true" alt="">
    <br />
    <a href="https://github.com/m1stborn/CPBL-Linebot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/m1stborn/CPBL-Linebot">View Demo</a>
    ·
    <a href="https://github.com/m1stborn/CPBL-Linebot/issues">Report Bug</a>
    ·
    <a href="https://github.com/m1stborn/CPBL-Linebot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#chat-command">Chat Command</a></li>
        <li><a href="#connect-to-line-notify">Tutorial - Connect to LINE Notify</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[//]: # ([![Product Name Screen Shot][product-screenshot]]&#40;https://example.com&#41;)

[//]: # (Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `m1stborn`, `CPBL-Linebot`, )

[//]: # (`twitter_handle`, `linkedin_username`, `gmail`, `kevin1997324`, `BaseMax`, `A LINE chatbot provide CPBL baseball live broadcast and game stats`)

在LINE上加入[BaseMax](https://lin.ee/VhvKZLS)帳號後，透過LINE聊天室快速掌握中華職棒比賽資訊!


主要功能:
1. 接收文字轉播: 透過LINE Notify接受中職的文字轉播(第一次使用需與LINE Notify連結帳號, [連結方式](#connect-to-line-notify))
2. 在聊天室中輸入[指令](#chat-command)可以查看各種當日賽事的數據
<div align="center">
    <br />
    <a href="https://lin.ee/VhvKZLS"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/zh-Hant.png" alt="加入好友" height="36" border="0"></a>
    <br />
    <img src="https://qr-official.line.me/sid/M/591tovcw.png?shortenUrl=true" alt="">
    <br />
</div>

<p align="right">(<a href="#top">back to top</a>)</p>

### Chat Command:
可以在聊天室輸入的指令<br />
- `今日賽事` - 查看今日比賽 - Today's game list
- `即時比數` - 查看目前比賽的比數 - Scoreboard in real time
- `球隊戰績` - 查看目前戰績排行 - standing
- `box` - 查看本場球員數據 - Box Score 
    - ex: `統一vs味全[打擊]`, `統一vs味全[投手]`

*需與LINE Notify連結帳號才能使用之指令
- `文字轉播` - 選擇想要轉播的比賽後從LINE Notify頻道接收文字轉播 - Live text broadcast
    - ex: `統一vs味全`

|             今日賽事              |             即時比數              |              文字轉播              |
|:-----------------------------:|:-----------------------------:|:------------------------------:|
| ![image](./assets/feat2.jpeg) | ![image](./assets/feat3.jpeg) | ![image](./assets/feat5.jpeg)  |

| 戰績排行                          | 數據盒子                          | 分享好友                           |
|-------------------------------|-------------------------------|--------------------------------|
| ![image](./assets/feat1.jpeg) | ![image](./assets/feat7.jpeg) | ![image](./assets/feat11.jpeg) |

<p align="right">(<a href="#top">back to top</a>)</p>

### Connect to LINE Notify:
(WIP)

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

* ![python][python-shield]
* ![Flask][flask-shield]
* ![Line][line-shield]
* ![Heroku][heroku-shield]
* ![Docker][docker-shield]
* ![GoogleCloud][googlecloud-shield]


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [X] Live game broadcast: 
- [X] Realtime game stats:
  - today's games info
  - scoreboard
  - batter/pitcher box score 
- [X] Sharing button
- [ ] Historical Game Database


See the [open issues](https://github.com/m1stborn/CPBL-Linebot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



[//]: # (<!-- LICENSE -->)

[//]: # (## License)

[//]: # ()
[//]: # (Distributed under the MIT License. See `LICENSE.txt` for more information.)

[//]: # ()
[//]: # (<p align="right">&#40;<a href="#top">back to top</a>&#41;</p>)



<!-- CONTACT -->
## Contact

Kevin Chang - kevin1997324@gmail.com

Project Link: [https://github.com/m1stborn/CPBL-Linebot](https://github.com/m1stborn/CPBL-Linebot)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/m1stborn/CPBL-Linebot.svg?style=for-the-badge
[contributors-url]: https://github.com/m1stborn/CPBL-Linebot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/m1stborn/CPBL-Linebot.svg?style=for-the-badge
[forks-url]: https://github.com/m1stborn/CPBL-Linebot/network/members
[stars-shield]: https://img.shields.io/github/stars/m1stborn/CPBL-Linebot.svg?style=for-the-badge
[stars-url]: https://github.com/m1stborn/CPBL-Linebot/stargazers
[issues-shield]: https://img.shields.io/github/issues/m1stborn/CPBL-Linebot.svg?style=for-the-badge
[issues-url]: https://github.com/m1stborn/CPBL-Linebot/issues
[license-shield]: https://img.shields.io/github/license/m1stborn/CPBL-Linebot.svg?style=for-the-badge
[license-url]: https://github.com/m1stborn/CPBL-Linebot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com

[//]: # ([python-shield-square]: https://img.shields.io/badge/python-3.8-blue.svg?style=for-the-badge)
[//]: # ([flask-shield-square]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
[//]: # ([docker-shield-square]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[//]: # ([googlecloud-shield-square]: https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
[//]: # ([heroku-shield-square]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
[//]: # ([line-shield-square]: https://img.shields.io/badge/Line-00C300?style=for-the-badge&logo=line&logoColor=white)

[python-shield]: https://img.shields.io/badge/python-3.8-blue.svg?style=for-the-badge
[flask-shield]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[docker-shield]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[googlecloud-shield]: https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white
[heroku-shield]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white
[line-shield]: https://img.shields.io/badge/Line-00C300?style=for-the-badge&logo=line&logoColor=white


[//]: # ([python-shield]: https://img.shields.io/badge/python-3.8-blue.svg?style=flat)
[//]: # ([flask-shield]: https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
[//]: # ([docker-shield]: https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
[//]: # ([googlecloud-shield]: https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=flat&logo=google-cloud&logoColor=white)
[//]: # ([heroku-shield]: https://img.shields.io/badge/heroku-%23430098.svg?style=flat&logo=heroku&logoColor=white)
[//]: # ([line-shield]: https://img.shields.io/badge/Line-00C300?style=flat&logo=line&logoColor=white)

[product-screenshot]: assets/feat2.jpeg
