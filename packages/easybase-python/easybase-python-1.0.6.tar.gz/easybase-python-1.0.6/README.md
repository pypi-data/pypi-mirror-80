
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/easybase/easybase-python">
    <img src="https://easybase.io/assets/images/logo_black.png" alt="Logo" width="80" height="80">
  </a>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
Python library to make REST requests to EasyBase.io. Although this library is not necessary to interface with EasyBase, it makes it Python integration much simpler.


### Built With

* [requests](https://requests.readthedocs.io/en/master/)
* [EasyBase.io](https://easybase.io)


<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip
* Python 3

### Installation
```python
pip install easybase-python
```



<!-- USAGE EXAMPLES -->
## Usage

```python
from easybase import get, post, update, delete

limit = 10
password = "my_integration_pass"
get_id = "sF7sh78sd_sdf7"

get_res = get(get_id, limit=limit, authenticaion=password)
print(get_res) # <- JSON
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/easybase/easybase-python/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/EasybaseFeature`)
3. Commit your Changes (`git commit -m 'feature'`)
4. Push to the Branch (`git push origin feature/EasybaseFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@easybase_io](https://twitter.com/easybase_io) - hello@easybase.io

Project Link: [https://github.com/easybase/easybase-python](https://github.com/easybase/easybase-python)
