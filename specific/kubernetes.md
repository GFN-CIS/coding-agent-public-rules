1. Don't make _helpers.tpl boierplate. Split it into meaningful files.
1. Prefer not to declare persistent data within the same release as application. The persistent data (pv/pvc/etc) should be in separate release because application reelases could be uninstalled during standart development process
