# Xtream_build
Instructions for building executables for XtreamCodes

### PECL install package
```/home/xtreamcodes/bin/php/bin/pecl install package```

### Build release
``` sudo python3 create_release.py```

---

## 🔧 **Automatic build and publish installation binaries**
We use **GitHub Actions** to automatically build and publish binaries to the repository [Xtream_install](https://github.com/Vateron-Media/Xtream_install) when a new tag is posted.

### 🔹 **Creating a release**
1. Go to the local Xtream_install repository
2. Tag the new version:
   ```sh
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. GitHub Actions will run the build and publish the compiled binary to [Releases](https://github.com/Vateron-Media/Xtream_install/releases).