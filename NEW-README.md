[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RomiconEZ/README-Template">
    <img src="images/mainlogo.jpg" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">GroupMyText</h3>

  <p align="center">
    Cluster your documents easily!
    <br />
    <br />
    <a href="https://github.com/RomiconEZ/README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/RomiconEZ/README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents / Содержание</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
        <ul>
        <li><a href="#Prerequisites">Prerequisites</a></li>
      </ul>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project / О проекте

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With / Технологический стек

* [![Next][Next.js]][Next-url]
* ![Python][Python.com]
* [![React][React.js]][React-url]
* ![fastapi][fastapi.com]
* ![Redis][Redis.com]
* ![Postgres][Postgres.com]
* ![Docker][Docker.com]
* [![AnaText][AnaText.github]][AnaText-url]




<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started / Начало 

### Prerequisites
- Docker: https://www.docker.com/get-started

### Installation / Установка

1. Clone the repository containing the source code for the backend and frontend apps.

2. Copy the `frontend/.env.example` file in the frontend directory and change the name to `.env`. Also, copy the `.env.example` file in the root directory of the repository and change the name to `.env`.
   - Change the OPENAI_API_KEY and OPENAI_ORGANIZATION to your own (n.b. OPENAI_ORGANIZATION should be your OpenAI 'Organization ID')

3. In the terminal, navigate to the root directory of the cloned repository. Build and start the Docker containers with the following command:
   ```
   docker-compose -f docker-compose.yml up -d
   ```
   Wait for the containers to build and start, which may take a few minutes depending on your system. Once the containers are up and running, you can access the apps in your browser at [http://localhost](http://localhost/).


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact / Контакты

Roman Neronov:
* email: roman.nieronov@gmail.com / roman.nieronov@mail.ru
* telegram: @Romiconchik

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/RomiconEZ/README-template.svg?style=for-the-badge
[contributors-url]: https://github.com/RomiconEZ/README-template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RomiconEZ/README-template.svg?style=for-the-badge
[forks-url]: https://github.com/RomiconEZ/README-template/network/members
[stars-shield]: https://img.shields.io/github/stars/RomiconEZ/README-template.svg?style=for-the-badge
[stars-url]: https://github.com/RomiconEZ/README-template/stargazers
[issues-shield]: https://img.shields.io/github/issues/RomiconEZ/README-template.svg?style=for-the-badge
[issues-url]: https://github.com/RomiconEZ/README-template/issues
[license-shield]: https://img.shields.io/github/license/RomiconEZ/README-template.svg?style=for-the-badge
[license-url]: https://github.com/RomiconEZ/README-template/blob/master/LICENSE.txt
[product-screenshot]: images/mainlogo.jpg
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

[Python.com]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white

[fastapi.com]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[Redis.com]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white

[Postgres.com]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[Docker.com]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[AnaText.github]: https://img.shields.io/badge/RomiconEZ-AnaText-orange

[AnaText-url]: https://github.com/RomiconEZ/AnaText
