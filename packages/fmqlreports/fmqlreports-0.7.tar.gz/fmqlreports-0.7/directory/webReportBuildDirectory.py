#!/usr/bin/env python
# -*- coding: utf8 -*-

#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import io
import json
from collections import defaultdict, Counter
from datetime import datetime

import pandas as pd

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL 
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent
from fmqlreports.webReportUtils import SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats, roundFloat
from fmqlreports.webReportUtils import muPlotRef, makePlots, vistasOfVISNByOne

from webReportUserDirectory import csvDatesBySNO
from buildDirectory import CommonBuildDirectory
from fileDirectory import CommonFileDirectory
                
"""
Build Directory
"""

# ###################################### Totals  ############################

PLOT_PREFIX = "visn20Build"

def makeTotalsSection(cd, vistaNames, imageDir="Images", fileDirectory=None):
                       
    plotData = {}
    
    bldIds = cd.buildIds()
                       
    mu = "## Build Breakdown\n\n"
             
    countsFromTotal = {
        "__entityName": "Builds",
    
        "__total": len(bldIds),
            
        "W/ Files": len(cd.buildsWithFiles()),
        "W/ Package": len(cd.buildsWithPackage()),
        "W/ Distribution Date": len(cd.buildEntryDates())
    }
    plotData["buildPercs"] = {
            "title": f'{countsFromTotal["__total"]} Builds',
            "plotName": f'{PLOT_PREFIX}Percs',
            "plotMethod": "plotIsHasBH",
            "specs": countsFromTotal
    }
    buildFiles = cd.buildFiles()
    blurb = "The directory holds <span class='yellowIt'>{:,}</span> distinct builds in <span class='yellowIt'>{:,}</span> packages. The builds create, change or populate <span class='yellowIt'>{:,}</span> files which represents <span class='yellowIt'>{}</span> of the files in VISN 20 systems. As can be seen here, most builds specify a distribution date and are in a package but a minority contain files".format(
        countsFromTotal["__total"],
        len(cd.buildPackages()),
        len(buildFiles),
        reportPercent(len(buildFiles), len(fileDirectory.fileIds()))
    )
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(plotData["buildPercs"], imageDir)
    )
     
    commonTotals = defaultdict(dict) # not picturing           
    allCnt = len(cd.vistas())
    for vistaInfo in cd.vistas():
        stationNo = vistaInfo["stationNumber"]
        stationMN = vistaNames[stationNo]
        commonCountsNos = cd.commonCounts(stationNo)
        commonCountsPer = {
            "all": commonCountsNos[allCnt],
            "some": sum(commonCountsNos[i] for i in range(2, allCnt)),
            "exclusive": commonCountsNos[1]
        }
        commonTotals[stationMN] = commonCountsPer
        
    plotData["commonByVistA"] = {
            "title": "Common Build Count",
            "plotName": f'{PLOT_PREFIX}Common',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals
    }
    blurb = "The graphic below shows the total number of builds in each system as well as a breakdown of whether those builds are unique to that system (exclusive), in some but not all systems (some) or in every (all) other systems in the directory. While the bigger systems like Puget Sound (PUG) have more builds, the vast majority of builds - <span class='yellowIt'>{}</span> - are shared by every VistA.".format(
        reportAbsAndPercent(commonTotals[list(commonTotals.keys())[0]]["all"], countsFromTotal["__total"])
    )
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistA"], imageDir)
    )
    
    plotData["commonByVistAPerc"] = {
            "title": "Common Build Count (Percentage)",
            "plotName": f'{PLOT_PREFIX}PercCommon',
            "plotMethod": "plotCategoryBSV",
            "specs": commonTotals,
            "kargs": { 
                "usePerc": True
            }
    }
    blurb = "The following shows the same information but instead of totals, each system's representation distinguishes the percentage of its builds that are unique from those that also appear elsewhere. It highlights that bigger systems have most of the exclusive builds, that there is something distinctive about them. _These distinctions need to be investigated_."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["commonByVistAPerc"], imageDir)
    )
        
    return plotData, mu
    
# #################################### Time Series Section ##########################

def makeTimeSeriesSection(cd, vistaNames, imageDir="Images"):

    plotData = {}
    
    end = "2020-02" # so common for all (make dynamic going forward)

    mu = "## Build Additions over Time\n\n"
    
    # For now (before get installs) just doing equivalent of catch all 'user'
    # done for user report ie/ build creation dates
    dailiesDFCSV = csvDatesBySNO(
        datesBySNO={"BUILD": sorted(cd.buildEntryDates().values())}
    )
        
    colNameById = {"BUILD": "Build"}
        
    plotData["ts365RollingMean"] = {
        "title": "Trends in Build Addition (365 day rolling)",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plot365RollingMean",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "colNameById": colNameById,
            "start": "1987-01", 
            "end": end
        }
    }
    blurb = "Here are the yearly trends using a __\"365 day rolling mean\"__. The build system started in 1996 and from then until 2006 produced the most builds. There was a sharp and steady decline until 2010. From that point on, build creation has been low but steady with a small blip in 2018."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["ts365RollingMean"],
            imageDir
        )
    )
    
    plotData["tsMonthlyResamples"] = {
        "title": "Builds - Resampled Monthly (2018 - {})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotMonthlyResamples",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "colNameById": colNameById,
            "start": '2018-01', 
            "end": end
        }
    }
    blurb = "When the data is __resampled by month__, you can see the 2018 _\"blip\"_ ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsMonthlyResamples"],
            imageDir
        )
    )
    
    plotData["tsTotalsPerYear"] = {
        "title": "Builds - Annual Creation (2015 - {})".format(re.sub(r'\-', '/', end)),
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotTotalsPerYear",
        "dfcsv": dailiesDFCSV,
        "kargs": {
            "colNameById": colNameById,
            "start": "2015", 
            "end": end,
            "snosOnly": False
        }
    }
    # TODO: calc these #'s - dangerous to just put here
    blurb = "Finally, a simple __set of totals__ for the last five years ..."
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsTotalsPerYear"],
            imageDir
        )
    )
                                    
    return plotData, mu
                    
# ############################## DRIVER ################################
            
def main():

    assert sys.version_info >= (3, 6)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "PLOT":
            makePlots("Common", "Builds")
            return
        raise Exception("Only argument allowed is 'PLOT'")

    visn20VistAs = vistasOfVISNByOne("20")

    dirName = "Build"
    cd = CommonBuildDirectory(visn20VistAs)

    plotData = {}
    mu = f"""---
layout: default
title: VISN 20 {dirName} Directory
---

# VISN 20 {dirName} Directory

"""

    mu += """The following reports on a VISN 20 Build Directory built from the build file (_9.6_) of 7 VistAs: Puget Sound [663], Portland [648], Boise [531], Spokane [668], Roseburg [653], White City [692] and Walla Walla [687]. Together they hold <span class='yellowIt'>{:,}</span> distinct builds using <span class='yellowIt'>{:,}</span> build file entries.

Note: Anchorage is the missing VISN 20 system. Its information will be added once the system is made available.

This directory should show [1] how VistA built up over time, [2] the extent to which the build system captures the contents of VistA and how [3] common VistAs are and the components that make them different.

""".format(
        cd.total(),
        cd.entryTotal()
    )
    
    ttlPlotData, ttlMU = makeTotalsSection(cd, visn20VistAs, fileDirectory=CommonFileDirectory(visn20VistAs))
    mu += ttlMU
    plotData.update(ttlPlotData)
    
    tsPlotData, tsMU = makeTimeSeriesSection(cd, visn20VistAs)
    mu += tsMU
    plotData.update(tsPlotData)
        
    plotDir = f'{VISTA_DATA_BASE_DIR}Common/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataBuilds.json', "w"), indent=4)
                
    siteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {siteDir}')
    open(f'{siteDir}visn20BuildDirectory.md', "w").write(mu) 
        
if __name__ == "__main__":
    main()
    
