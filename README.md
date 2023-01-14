# LineageOS static OTA

Simple script to create OTA updates for unofficial devices.

### Usage
1. Copy your build to `builds`
    - Make folder if it doesn't exist.
    - This folder can really be named anything, but `builds` is .gitignored, so we may as well stick to that.
    - Only one build per device. We don't need to check for any other builds, it's an OTA so there should only be one update visible to the end device.
1. Run `python3 gen_json.py builds <base URL of builds location>`
    - URL example:
        - if your build is on SourceForge, do `https://sourceforge.net/projects/your-project/files/`
    - **Limitation**: if you have multiple devices, this script assumes that your builds are all on the same base URL.
        - TODO granularize this
1. In the `api` directory, `<device>.json` is created. Upload this to wherever your website is located
    - You can directly use this project with GitHub Pages, and then the URL would be something similar to `https://raw.githubusercontent.com/<username>/lineage_ota/master/api/<device>.json`
1. In your device's system properties, set `lineage.updater.uri` to the URL of the JSON file that was just created
    - if you did not build with this set, the build you used to generate JSON in step 1 will not check for this. You can just re-run script after building ROM with this prop set.
