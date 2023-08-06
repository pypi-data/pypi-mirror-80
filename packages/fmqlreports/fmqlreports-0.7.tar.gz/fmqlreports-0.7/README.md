# fmqlreports

Reports from FMQL Data building on fmqlutils

## Installing

> pip3 install --upgrade --force-reinstall --user fmqlreports

## Generating Reports

  * [ ] basics
  * [ ] directories [Common]
  * [ ] user
  * [ ] visit
  * [ ] ifc

## Serving Report Site

Steps to create:

```text
> cp -r ReportSiteTemplate /data/vista/{SN}/ReportSite
> cd /data/vista/{SN}/ReportSite
> vi _config.yml (update title and port)
> jekyll serve
```

Note: blank index.md to start - need to generate in
