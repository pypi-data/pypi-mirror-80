import gdspy
import opthedgehog
from math import cos, sin, pi

if __name__ == "__main__":


    print("package testing")
    cell0 = gdspy.Cell("topcell")

    opthedgehog.config.dfoptwgwidth = 1.5
    opthedgehog.config.dfOptRes = 0.3

    # ========================  Electronic Footprint ======================
    opthedgehog.config.dfoptwgwidth = 20
    wg1 = opthedgehog.OptStraightWaveguide("wg1", inports=[(0,100,1,0.3)], length=1000, layer = 30)
    pad = opthedgehog.SMT2pin("C1", inports=wg1.outports, sizetype="0201", angle=90., layer = 3)
    wg2 = opthedgehog.OptStraightWaveguide("wg2", inports=pad.outports, length=1000, layer = 30)
    cell0.add(wg1)
    cell0.add(pad)
    cell0.add(wg2)


    # =========================  Suspended Cavity =====================================
    # wg1 = opthedgehog.SuspendOptStraightWaveguide("SuspendOptStraightWaveguide", inports=[(0, 0, 1., 0.2)], length=100.0, layer=1)
    # suscavity1 = opthedgehog.SuspendOptRingCavity("OptRingCavity", inports=[wg1.outports[0]],
    #                                            cavityradius=250,
    #                                            couplinggap=1.0, ringwidth=1.5, )
    #
    # bnd = opthedgehog.SuspendOptBezierConnect("OptBezierConnect", inports=suscavity1.outports, shift=(600, -400),
    #                                     outputdirection=(1.3, -1.0), layer=10)
    #
    # racecavity1 = opthedgehog.SuspendOptRaceTrackCavity("OptRaceTrackCavity", inports=bnd.outports,
    #                                          cavityCornerRadius=250.0, cavityLength=100.0, cavityWidth=2.0,
    #                                          couplinggap=1.0, ringwidth=1.5, direction=1, layer=10, suslayer = 20)
    #
    #
    # Ysplitter = opthedgehog.PosOptYsplitter("OptSuspendedYsplitter", racecavity1.outports, (200., 60.), )
    #
    # Ymerger = opthedgehog.SuspendOptYmerger("OptSuspendedYmerger", Ysplitter.outports, splitshift=200 )
    #
    # unitcellist = [gdspy.CellReference(i) for i in [wg1, suscavity1, bnd, racecavity1, Ysplitter, Ymerger]]
    # cell0.add(unitcellist)

    # ========================  PosOptDiskCavity ======================================
    # wg1 = opthedgehog.OptStraightWaveguide("OptStraightWaveguide", inports=[(0, 0, 1., 0.2)], length=100.0, layer=1)
    #
    # diskcavity1 = opthedgehog.PosOptDiskCavity("OptDiskCavity", inports=wg1.outports, cavityradius=50.0, couplinggap=2.0, direction=1, layer=2,
    #                                            openingPattern = 5.)
    #
    # diskcavity2 = opthedgehog.PosOptDiskCavity("OptDiskCavity2", inports=diskcavity1.outports, cavityradius=50.0, couplinggap=2.0, direction=-1, layer=2,
    #                                            openingPattern = 5.)
    #
    # unitcellist = [gdspy.CellReference(i) for i in [wg1, diskcavity1, diskcavity2]]
    # cell0.add(unitcellist)


    #========================  OptSuspnededFiberTipCoupler ======================================

    # fibertaper1 = opthedgehog.OptSuspnededFiberTipCoupler("OptSuspnededFiberTipCoupler", inports=[(1000., 100., -1., .5)], L1 = 40, W1=1.5, L2 = 25, S2 = 8, Ext=150.)
    #
    # wgT1 = opthedgehog.OptStraightWaveguide("wgT1", inports=fibertaper1.outports, length=500)
    #
    # fibertaper2 = opthedgehog.OptSuspnededFiberTipCoupler("OptSuspnededFiberTipCoupler", inports=wgT1.outports, L1=40, W1=1.5, L2=25, S2=8, Ext=150., reverse=True)
    #
    # unitcellist = [gdspy.CellReference(i) for i in [fibertaper1, wgT1, fibertaper2]]
    # cell0.add(unitcellist)


    #################### OptCurvedGratingCoupler ##########################
    # opthedgehog.config.dfPosOptCellOpening = 5.0
    #
    # Curvedgrt1 = opthedgehog.PosOptCurvedGratingCoupler("grating1", inports=[(0, 0, 1, 0.2)], gratingN= 20, gratingPeroid=1. )
    # Curvedgrt1.addLabel()
    # wgT1 = opthedgehog.PosOptStraightWaveguide("wgT1", inports=Curvedgrt1.outports, length=100)
    # Curvedgrt2 = opthedgehog.PosOptCurvedGratingCoupler("grating2", inports=wgT1.outports, gratingN=20, gratingPeroid=1., reverse=True)
    # Curvedgrt2.addLabel()
    #
    # unitcellist = [gdspy.CellReference(i) for i in [Curvedgrt1, wgT1, Curvedgrt2]]
    # cell0.add(unitcellist)



    ################## test of add on coupler ###############################
    # setting the resolution of polygon points in the gdsii files

#     wgX1 = opthedgehog.OptStraightWaveguide("wgX1", inports=[(0, 600, 1.0, 0.)], length=400)
#     wgX1.addLabel()
#     wgX2 = opthedgehog.PosOptStraightWaveguide("wgX2", inports=wgX1.outports, length=400, etchlayer=15, keepFirst=True)
#     wgX3 = opthedgehog.PosOptStraightWaveguide("wgX3", inports=wgX2.outports, length=400, keepFirst= True)
#
#     wgCpl1 = opthedgehog.OptStraightWaveguide("wgCpl1", inports=[(300, 750, 0.0, -1.0)], length=50)
#     wgCplX = opthedgehog.OptAddOnWaveguideCoupler("wgcplX", inports=wgCpl1.outports, couplingPos=wgX1.outports, couplingLength=50., couplingPitch=2.0)
#     wgCpl2 = opthedgehog.OptStraightWaveguide("wgCpl1", inports=wgCplX.outports, length=50)
#
#     wgCplp1 = opthedgehog.OptStraightWaveguide("wgCpl1", inports=[(600, 625, 1.0, 0.0)], length=100)
#     wgCplpX = opthedgehog.PosOptAddOnWaveguideCoupler("wgcplX", inports=wgCplp1.outports, couplingPos=wgX2.outports, couplingLength=50., couplingPitch=2.0,
#                                                       refPattern=[wgX2, wgX3])
#     wgCplp2 = opthedgehog.OptStraightWaveguide("wgCpl1", inports=wgCplpX.outports, length=50)
#
#     unitcellist = [gdspy.CellReference(i) for i in [wgX1, wgX2, wgX3, wgCpl1, wgCplX, wgCpl2, wgCplp1, wgCplpX, wgCplp2]]
#     cell0.add(unitcellist)
#
#     ####################  test of circular bend #######################################
#     wgC1 = opthedgehog.OptStraightWaveguide("wg1", inports=[(0, -400, 1.0, 0.0)], length=100)
#     wgCbend1 = opthedgehog.OptCircularBend("cbend1", inports=wgC1.outports, radius = 100.0, bendangle=90.0 )
#     wgC2 = opthedgehog.OptStraightWaveguide("wg2", inports=wgCbend1.outports, length=100)
#     wgCbend2 = opthedgehog.OptCircularBend("cbend2", inports=wgC2.outports, radius=100.0, bendangle=-90.0)
#     wgC3 = opthedgehog.OptStraightWaveguide("wg3", inports=wgCbend2.outports, length=500)
#     wgCbend3 = opthedgehog.OptCircularBend("cbend3", inports=wgC3.outports, radius=100.0, bendangle=-200.0)
#     wgCbend4 = opthedgehog.OptCircularBend("cbend4", inports=wgCbend3.outports, radius=100.0, bendangle=270.0)
#
#
#     unitcellist = [gdspy.CellReference(i) for i in [wgC1, wgCbend1, wgCbend2, wgC2, wgC3, wgCbend3, wgCbend4]]
#     cell0.add(unitcellist)
#
# ##########################   SPUDT  Feb 2020 ##################################################
#     SPUDT1 = opthedgehog.SPUDTcell("SPUDT1", width = 100.0, fingerpitch= 1.0, n = 20, direction=1, padlayer=1)
#     SPUDT2 = opthedgehog.SPUDTcell("SPUDT2", width=100.0, fingerpitch=1.0, n=20, direction=-1, padlayer=1)
#     cell0.add([gdspy.CellReference(SPUDT1, ( -500, -20 )), gdspy.CellReference(SPUDT2, ( -500, 20 ))])
#
# ##########################  OPTcell Jan 2020 #####################
#     opthedgehog.config.dfoptwgwidth = 2.0
#     opthedgehog.config.dfOptRes = 0.3   # setting the resolution of polygon points in the gdsii files
#
#     #testing a grating coupler pair
#     couplerG1 = opthedgehog.OptSimpleGratingCoupler("gratingA", inports=[(100, 300, 9.0, 0.5)], gratingN=40, gratingPeroid=0.8, gratingApod=True,
#                                                    gratingWidth=20.0, gratingDuty=0.25)
#     wgG1 = opthedgehog.SuspendOptStraightWaveguideAdvanced("wgG1", inports=couplerG1.outports, length = 2000.0, susOffset=5.0, susCon=1.0, susSeg=20.0, susWidth=1.0)
#     couplerG2 = opthedgehog.OptSimpleGratingCoupler("gratingA", inports=wgG1.outports, gratingN=40, gratingPeroid=0.8, gratingApod=False,
#                                                    gratingWidth=20.0, gratingDuty=0.6, reverse=True)
#
#     #examples for some components
#     tapercoupler = opthedgehog.OptSimpleGratingCoupler("garting1",inports=[(0, 0, 2.345, 0.0)], gratingN= 30, gratingPeroid= 1.0, reverse=False)
#
#     wg1 = opthedgehog.SuspendOptStraightWaveguideAdvanced("wg1", inports=tapercoupler.outports, length = 100.0)
#
#     wg1b = opthedgehog.OptStraightWaveguide("wg1b", inports=[(0,-50,1,0.0)], length = 100.0)
#
#     coupler = opthedgehog.OptWaveguideCoupler("coupler", inports=[*wg1.outports, *wg1b.outports], taperLength=100.0, couplingLength=100.0, couplingGap=0.5)
#
#     #special case, zero coupling gap
#     coupler3 = opthedgehog.OptWaveguideCoupler("coupler3", inports=coupler.outports, taperLength=200.0, couplingLength=100.0,  couplingGap=-opthedgehog.config.dfoptwgwidth)
#
#     #special usage of OptWaveguideCoupler, set coupling gap very large and use same coordinate for both ports,to make MZI,
#     coupler2 = opthedgehog.OptWaveguideCoupler("coupler2", inports=[coupler3.outports[0], coupler3.outports[0]], taperLength=200.0, couplingLength=200.0, couplingGap=50)
#
#
#     cavity1 = opthedgehog.OptRingCavity("cavity1", inports=coupler2.outports, cavityradius=100.0, couplinggap=0.5)
#
#     wg2 = opthedgehog.OptStraightWaveguide("wg2", inports=cavity1.outports, length=100.0)
#
#     cavity2 = opthedgehog.OptRingCavity("cavity2", inports=wg2.outports, cavityradius=100.0, couplinggap=2.0, direction=-1)
#
#     opthedgehog.config.dfTurningRadius = 120
#     wg3 = opthedgehog.OptBezierConnect("bend3", inports=cavity2.outports, shift=(300,-50), outputdirection=(2.0, -0.5))
#
#     cavityR3 = opthedgehog.OptRaceTrackCavity("cavityR3", inports=wg3.outports,
#                                               cavityCornerRadius=50.0, cavityLength=200.0, cavityWidth=0.0, couplinggap=1.0)
#
#     cavityR4 = opthedgehog.OptRaceTrackCavity("cavityR3", inports=cavityR3.outports,
#                                               cavityCornerRadius=30.0, cavityLength=0.0, cavityWidth=20.0, couplinggap=1.0, ringwidth=0.5,direction=-1)
#
#     tapercouplerOUT = opthedgehog.OptSimpleGratingCoupler("garting1", inports=cavityR4.outports, gratingN=30, gratingPeroid=1.0, reverse=True)
#
#     unitcellist = [gdspy.CellReference(i) for i in [couplerG1, wgG1, couplerG2, tapercoupler, wg1, wg1b, coupler, coupler3, coupler2, cavity1, wg2, cavity2, wg3, cavityR3, cavityR4, tapercouplerOUT]]
#     cell0.add(unitcellist)

######################  TESTING  -- acoustic cells ###############
    # opthedgehog.config.dfoptwgwidth = 5.0
    # opthedgehog.config.dfOptRes = 0.1
    # Awg1 = opthedgehog.OptStraightWaveguide("wg1", [(0,0,1,0)], 500.0, endwidth=10.0)
    # Awg2 = opthedgehog.OptStraightWaveguide("wg2", Awg1.outports, 500.0, endwidth=5.0)
    # bend3 = opthedgehog.OptBezierWaveguide("wg3", Awg2.outports, [(100, 0), (200, 0), (250, 50)])
    # Ysplit = opthedgehog.OptYsplitter("Ysplit",bend3.outports,(300, 100))
    # Awg4 = opthedgehog.OptStraightWaveguide("wg4", Ysplit.outports[1], 20.0, endwidth=5.0)
    # Awg5 = opthedgehog.OptStraightWaveguide("wg5", Ysplit.outports[0], 20.0, endwidth=5.0)
    # Ymerger = opthedgehog.OptYmerger("Ymerger", [*Awg4.outports, *Awg5.outports], 300)
    #
    # unitcellist = [gdspy.CellReference(i) for i in [Awg1, Awg2, bend3, Ysplit, Awg4, Awg5, Ymerger]]
    # cell0.add(unitcellist)

############################ testing Align Check Marker
    #cell0.add(gdspy.CellReference(opthedgehog.alignCheckMarker()))

####################################
# testing code for Yaowen
####################################
    # opthedgehog.config.dfoptwgwidth = 1.20  # waveguide width
    # opthedgehog.config.dfTurningRadius = 50.0  # reference turning radius for curves
    #
    # #
    # startingPos = [(0, -1000, 1, 0)]
    # #
    #
    # opthedgehog.config.dfoptwgwidth = 3.00  # waveguide width
    # wgc = opthedgehog.OptStraightWaveguide("wgc", inports=startingPos , length= 300.0)
    # bendc = opthedgehog.OptBezierConnect("bend5", inports=wgc.outports, shift=(100, 100), outputdirection=(1.0, 0), layer=10)
    #
    # Ysplit = opthedgehog.OptYsplitter("Ysplit", inports=bendc.outports,splitshift=(500.0,30.0))
    # bendd = opthedgehog.OptBezierConnect("bend6", inports=Ysplit.outports[1], shift=(100, 300), outputdirection=(1.0, 0.0), layer=10)
    #
    # Ymerge = opthedgehog.OptYmerger("Ymerge", inports=[bendd.outports[0], Ysplit.outports[0]] , shift= 600.0 )
    #
    # bend3 = opthedgehog.OptBezierWaveguide("wg3", Ymerge.outports, [(100, 0), (200, 0), (250, 50)])
    #
    # unitcellist = [gdspy.CellReference(i) for i in [wgc, bendc, bendd, Ysplit,Ymerge ]]
    # cell0.add(unitcellist)
    # #
    # alignment = opthedgehog.alignmentMarker("alignment1", layer = 10)
    # cell0.add([gdspy.CellReference(alignment, origin=(-500,1000)), gdspy.CellReference(alignment, origin=(1500,-1500))])
    #

#########################  test for Pos LEns
    # lens = opthedgehog.PosOptEllipseLens("lens",flens=50.0, ep = 0.8617, width = 200.0)
    # unitcellist = [gdspy.CellReference(i) for i in [lens]]
    # cell0.add(unitcellist)


######################### test for MMI ################################
    # starting1 = (0.0, 30.0,1.0,0.0)
    # starting2 = (0.0, -30.0, 1.0, 0.0)
    # wg1 = opthedgehog.SuspendOptStraightWaveguide("wg1", inports=starting1, length=200.0)
    # wg2 = opthedgehog.SuspendOptStraightWaveguide("wg2", inports=starting2, length=200.0)
    # mixer = opthedgehog.PosOpt2x2MMI("mmi1",inports=[wg1.outports[0],wg2.outports[0]],
    #                               endwgwidth=3.5, MMIwidth=7.0, MMIlength=40.0, MMIinputoffset=1.75, etchlayer = 15)
    #
    # wg3 = opthedgehog.SuspendOptStraightWaveguide("wg3", inports=mixer.outports[0], length=200.0)
    # wg4 = opthedgehog.SuspendOptStraightWaveguide("wg4", inports=mixer.outports[1], length=200.0)
    #
    # unitcellist = [gdspy.CellReference(i) for i in [wg1, wg2, mixer,wg3,wg4]]
    # cell0.add(unitcellist)

########################## test for suspended optical WG with electric drive
    # starting = (-0.0, 0.0, 1.0, 0.0)
    # wg1 = opthedgehog.SuspendOptStraightWaveguide("wg1", inports=starting, length=200.0)
    # mod1 = opthedgehog.AcoustoOptStraight4SegWaveguide("AOLongwg",
    #                                                inports=wg1.outports,
    #                                                slabSingleLength=150.0,
    #                                                slabWidth=10.0,
    #                                                IDToffset=3.0,
    #                                                IDTn=4)
    # wg2 = opthedgehog.SuspendOptStraightWaveguide("wg2", inports=mod1.outports, length=200.0)
    # unitcellist = [gdspy.CellReference(i) for i in [wg1, mod1, wg2]]
    # cell0.add(unitcellist)



#########################  test of waveguide at any angle #######################
    # angle = pi
    # direction = (cos(angle), -sin(angle))
    # starting = (-1000.0, 1000.0, 1.0, 0.0)
    # wg1 = opthedgehog.OptStraightWaveguide("wg1",inports=starting, length= 100.0)
    # wg1bend = opthedgehog.OptBezierConnect("wg1bend", inports=wg1.outports, shift=(200.0, -200.0), outputdirection= direction)
    # wg2 = opthedgehog.OptStraightWaveguide("wg2",inports=wg1bend.outports, length= 100.0)
    # # wgtaper = opthedgehog.PosOptTaper("wgtaper1", inports=wg2.outports, length = 300.0, startwidth=opthedgehog.config.dfoptwgwidth, endwidth=30.0, alpha = 2.0)
    # # opthedgehog.config.dfoptwgwidth = 30.0
    # # wg3 = opthedgehog.PosOptStraightWaveguide("wg3",inports=wgtaper.outports, length= 100.0)
    #
    # unitcellist = [gdspy.CellReference(i) for i in [wg1, wg1bend, wg2]]
    # # unitcellist = [gdspy.CellReference(i) for i in [wg1 ]]
    # cell0.add( unitcellist )



###########################  test of IDT pads #################################
    # IDT = opthedgehog.IDTcell("testIDT", width = 500.0, fingerwidth=1.0, fingerpitch=2.0, n = 100)
    # cell0.add(gdspy.CellReference(IDT))

########### test SuspendedTaperCoupler #####################
    # tapercoupler1 = opthedgehog.SuspendedTaperCoupler("taper",WG1cell.inports, wgtaper=30, wgtaperend=0.1, slabtaper=60, slabend=0.2, direction = -1, taperp = 2.0, totiplength=100.0)
    # cell0.add(tapercoupler1)


########## test coupled cavities  ####################
    # inports1 = [WG1cell.outports[0], WG1cel2.outports[0]]
    # # coupledCavity = opthedgehog.AcoustoOptSusCoupledRaceTrack("coupled", inport=inports1, cavityradius=110.0, cavityRacinglength=100.0, WGcplGap=1.20,
    # #                                                cavitycplGap=3.0, ringwidth =1.2, slabLength=90.0, slabWidth=15.0, IDToffset=3.0, IDTn = 4)
    #
    # #coupledCavity = opthedgehog.OptSingleEMAORaceTrack("coupled", inport=inports1, cavityradius=110.0, cavityRacinglength=100.0, WGcplGap=1.20,
    # #                                                           ringwidth=1.3)
    # coupledCavity = opthedgehog.AcoustoOptSusSingleRaceTrack("single", inport=inports1, cavityradius=100.0, cavityRacinglength=100.0, WGcplGap=1.20,
    #                                                  ringwidth =1.3, slabLength=90.0, slabWidth=10.0, IDToffset=3.0, IDTn = 4)
    #
    #
    # cell0.add(coupledCavity)
    # print("  [test info] coupled cavities added "+str(coupledCavity.outports))
    # print("  [test DEBUG] ")


######### test tracing track cavity with SAW ##############

    # cavityRacing = opthedgehog.AcoustoOptSuspendedOptRaceTrackCavityVC("trackingCavity", WG1cell.outports, 100.0, 150.0, 0.4, 90.0, 30.0, 5.0, 4)
    # cell0.add(cavityRacing)
    # print(" [test Info] Suspended Racing cavity added. OUT port: "+str(cavityRacing.outports))
#
# # #################   bended waveguide ###############
#     WG2cell = opthedgehog.SuspendOptParallelBezierConnect("wg2",cavityRacing.outports, (200,100))
#     cell0.add(WG2cell)
#     print(" [test Info] Bended optical waveguide. OUT port:"+str(WG2cell.outports))
#
# # #################   Ring cavity  #############
#     cavity1 = opthedgehog.SuspendOptRingCavity("cavity1",inport= WG2cell.outports, ringwidth=1.5, cavityradius=100.0, couplinggap= 0.45, direction=1)
#     cell0.add(cavity1)
#     print("  [test INFO] add ring resonator. OUT port:"+str(cavity1.outports))
#
# # ################   Y splitter  ##############
#     Ycell3 = opthedgehog.SuspendOptYsplitter("splitter", (0,0,1,0) , (700, 50))
#     cell0.add( gdspy.CellReference(Ycell3))
#     print("  [test INFO]   Y splitter out ports list:  "+str(Ycell3.outports))
#
# # ################    SAW - waveguide coupling slab ###############
#     AOStraightwg = opthedgehog.AcoustoOptStraightWaveguide("extendwg", Ycell3.outports[0], 200, 10.0, 2.0, 4)
#     cell0.add(AOStraightwg)
#     print("  [test INFO]  SAW coupled straight waveguide:  " + str(AOStraightwg.outports))
#
# # ################   Waveguide 4 ########################
#     WG4cell = opthedgehog.SuspendOptStraightWaveguide("wg4", Ycell3.outports[1], 210)
#     cell0.add(WG4cell)
#     print("  [test INFO]  straight waveguide:" + str(WG4cell.outports))
#
# # ################    Y merger ##########################
#     Ycell4 = opthedgehog.SuspendOptYmerger("merger", [WG4cell.outports[0], AOStraightwg.outports[0]], (700, 0))
#     cell0.add(Ycell4)
#     print("  [test INFO]   Y merger out ports list:  " + str(Ycell4.outports))
#
#
# ################  taper coupler ########################
#     tapercoupler2 = opthedgehog.SuspendedTaperCoupler("taper", Ycell4.outports, wgtaper=30, wgtaperend=0.1, slabtaper=60, slabend=0.2, direction=1, taperp=2.0)
#     cell0.add(tapercoupler2)

##### test alignment marker
    # cell0.add(OptHedgehog.alignmentMarker())

    #    gdspy.LayoutViewer()
    #cell0_flattern = cell0.flatten()
    #gdspy.write_gds("test.gds",cells=[cell0_flattern])

    gdspy.write_gds("test.gds", unit=1e-6, precision=1e-10)

    print(" --- finished ---")

