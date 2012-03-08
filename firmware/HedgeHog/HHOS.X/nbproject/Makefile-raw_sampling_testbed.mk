#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-raw_sampling_testbed.mk)" "nbproject/Makefile-local-raw_sampling_testbed.mk"
include nbproject/Makefile-local-raw_sampling_testbed.mk
endif

# Environment
MKDIR=mkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=raw_sampling_testbed
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=cof
DEBUGGABLE_SUFFIX=cof
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=cof
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/797530045/oled.o ${OBJECTDIR}/_ext/1472/display_config.o ${OBJECTDIR}/_ext/247156599/SD-SPI.o ${OBJECTDIR}/_ext/34024445/BMA150.o ${OBJECTDIR}/_ext/677419432/ambient_light.o ${OBJECTDIR}/_ext/82867227/usb_device.o ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o ${OBJECTDIR}/_ext/983254276/usb_function_msd.o ${OBJECTDIR}/_ext/2138657381/SD_FAT.o ${OBJECTDIR}/_ext/1472/osc.o ${OBJECTDIR}/_ext/1360904562/rtcc.o ${OBJECTDIR}/_ext/1472/usb_descriptors.o ${OBJECTDIR}/_ext/1472/config_cdc.o ${OBJECTDIR}/_ext/1472/HHG_conf.o ${OBJECTDIR}/_ext/1472/SD_Buffer.o ${OBJECTDIR}/_ext/1472/main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/797530045/oled.o.d ${OBJECTDIR}/_ext/1472/display_config.o.d ${OBJECTDIR}/_ext/247156599/SD-SPI.o.d ${OBJECTDIR}/_ext/34024445/BMA150.o.d ${OBJECTDIR}/_ext/677419432/ambient_light.o.d ${OBJECTDIR}/_ext/82867227/usb_device.o.d ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o.d ${OBJECTDIR}/_ext/983254276/usb_function_msd.o.d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d ${OBJECTDIR}/_ext/1472/osc.o.d ${OBJECTDIR}/_ext/1360904562/rtcc.o.d ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d ${OBJECTDIR}/_ext/1472/config_cdc.o.d ${OBJECTDIR}/_ext/1472/HHG_conf.o.d ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d ${OBJECTDIR}/_ext/1472/main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/797530045/oled.o ${OBJECTDIR}/_ext/1472/display_config.o ${OBJECTDIR}/_ext/247156599/SD-SPI.o ${OBJECTDIR}/_ext/34024445/BMA150.o ${OBJECTDIR}/_ext/677419432/ambient_light.o ${OBJECTDIR}/_ext/82867227/usb_device.o ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o ${OBJECTDIR}/_ext/983254276/usb_function_msd.o ${OBJECTDIR}/_ext/2138657381/SD_FAT.o ${OBJECTDIR}/_ext/1472/osc.o ${OBJECTDIR}/_ext/1360904562/rtcc.o ${OBJECTDIR}/_ext/1472/usb_descriptors.o ${OBJECTDIR}/_ext/1472/config_cdc.o ${OBJECTDIR}/_ext/1472/HHG_conf.o ${OBJECTDIR}/_ext/1472/SD_Buffer.o ${OBJECTDIR}/_ext/1472/main.o


CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
	${MAKE}  -f nbproject/Makefile-raw_sampling_testbed.mk dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=18F46J50
MP_PROCESSOR_OPTION_LD=18f46j50
MP_LINKER_DEBUG_OPTION=
# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/797530045/oled.o: ../OLED\ driver/oled.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/797530045 
	@${RM} ${OBJECTDIR}/_ext/797530045/oled.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/797530045/oled.o   "../OLED driver/oled.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/797530045/oled.o 
	
${OBJECTDIR}/_ext/1472/display_config.o: ../display_config.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/display_config.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/display_config.o   ../display_config.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/display_config.o 
	
${OBJECTDIR}/_ext/247156599/SD-SPI.o: /opt/microchip/Microchip/MDD\ File\ System/SD-SPI.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/247156599 
	@${RM} ${OBJECTDIR}/_ext/247156599/SD-SPI.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/247156599/SD-SPI.o   "/opt/microchip/Microchip/MDD File System/SD-SPI.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/247156599/SD-SPI.o 
	
${OBJECTDIR}/_ext/34024445/BMA150.o: ../BMA150\ driver/BMA150.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/34024445 
	@${RM} ${OBJECTDIR}/_ext/34024445/BMA150.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/34024445/BMA150.o   "../BMA150 driver/BMA150.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/34024445/BMA150.o 
	
${OBJECTDIR}/_ext/677419432/ambient_light.o: ../ambient_light\ driver/ambient_light.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/677419432 
	@${RM} ${OBJECTDIR}/_ext/677419432/ambient_light.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/677419432/ambient_light.o   "../ambient_light driver/ambient_light.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/677419432/ambient_light.o 
	
${OBJECTDIR}/_ext/82867227/usb_device.o: /opt/microchip/Microchip/USB/usb_device.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/82867227 
	@${RM} ${OBJECTDIR}/_ext/82867227/usb_device.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/82867227/usb_device.o   /opt/microchip/Microchip/USB/usb_device.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/82867227/usb_device.o 
	
${OBJECTDIR}/_ext/224044192/usb_function_cdc.o: /opt/microchip/Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/224044192 
	@${RM} ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o   "/opt/microchip/Microchip/USB/CDC Device Driver/usb_function_cdc.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o 
	
${OBJECTDIR}/_ext/983254276/usb_function_msd.o: /opt/microchip/Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/983254276 
	@${RM} ${OBJECTDIR}/_ext/983254276/usb_function_msd.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/983254276/usb_function_msd.o   "/opt/microchip/Microchip/USB/MSD Device Driver/usb_function_msd.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/983254276/usb_function_msd.o 
	
${OBJECTDIR}/_ext/2138657381/SD_FAT.o: ../../HedgeHog/SD_FAT.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/2138657381 
	@${RM} ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/2138657381/SD_FAT.o   ../../HedgeHog/SD_FAT.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o 
	
${OBJECTDIR}/_ext/1472/osc.o: ../osc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/osc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/osc.o   ../osc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/osc.o 
	
${OBJECTDIR}/_ext/1360904562/rtcc.o: ../RTC/rtcc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1360904562 
	@${RM} ${OBJECTDIR}/_ext/1360904562/rtcc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1360904562/rtcc.o   ../RTC/rtcc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1360904562/rtcc.o 
	
${OBJECTDIR}/_ext/1472/usb_descriptors.o: ../usb_descriptors.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/usb_descriptors.o   ../usb_descriptors.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/usb_descriptors.o 
	
${OBJECTDIR}/_ext/1472/config_cdc.o: ../config_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/config_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/config_cdc.o   ../config_cdc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/config_cdc.o 
	
${OBJECTDIR}/_ext/1472/HHG_conf.o: ../HHG_conf.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/HHG_conf.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/HHG_conf.o   ../HHG_conf.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/HHG_conf.o 
	
${OBJECTDIR}/_ext/1472/SD_Buffer.o: ../SD_Buffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/SD_Buffer.o   ../SD_Buffer.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/SD_Buffer.o 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/main.o   ../main.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/main.o 
	
else
${OBJECTDIR}/_ext/797530045/oled.o: ../OLED\ driver/oled.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/797530045 
	@${RM} ${OBJECTDIR}/_ext/797530045/oled.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/797530045/oled.o   "../OLED driver/oled.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/797530045/oled.o 
	
${OBJECTDIR}/_ext/1472/display_config.o: ../display_config.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/display_config.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/display_config.o   ../display_config.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/display_config.o 
	
${OBJECTDIR}/_ext/247156599/SD-SPI.o: /opt/microchip/Microchip/MDD\ File\ System/SD-SPI.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/247156599 
	@${RM} ${OBJECTDIR}/_ext/247156599/SD-SPI.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/247156599/SD-SPI.o   "/opt/microchip/Microchip/MDD File System/SD-SPI.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/247156599/SD-SPI.o 
	
${OBJECTDIR}/_ext/34024445/BMA150.o: ../BMA150\ driver/BMA150.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/34024445 
	@${RM} ${OBJECTDIR}/_ext/34024445/BMA150.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/34024445/BMA150.o   "../BMA150 driver/BMA150.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/34024445/BMA150.o 
	
${OBJECTDIR}/_ext/677419432/ambient_light.o: ../ambient_light\ driver/ambient_light.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/677419432 
	@${RM} ${OBJECTDIR}/_ext/677419432/ambient_light.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/677419432/ambient_light.o   "../ambient_light driver/ambient_light.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/677419432/ambient_light.o 
	
${OBJECTDIR}/_ext/82867227/usb_device.o: /opt/microchip/Microchip/USB/usb_device.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/82867227 
	@${RM} ${OBJECTDIR}/_ext/82867227/usb_device.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/82867227/usb_device.o   /opt/microchip/Microchip/USB/usb_device.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/82867227/usb_device.o 
	
${OBJECTDIR}/_ext/224044192/usb_function_cdc.o: /opt/microchip/Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/224044192 
	@${RM} ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o   "/opt/microchip/Microchip/USB/CDC Device Driver/usb_function_cdc.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/224044192/usb_function_cdc.o 
	
${OBJECTDIR}/_ext/983254276/usb_function_msd.o: /opt/microchip/Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/983254276 
	@${RM} ${OBJECTDIR}/_ext/983254276/usb_function_msd.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/983254276/usb_function_msd.o   "/opt/microchip/Microchip/USB/MSD Device Driver/usb_function_msd.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/983254276/usb_function_msd.o 
	
${OBJECTDIR}/_ext/2138657381/SD_FAT.o: ../../HedgeHog/SD_FAT.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/2138657381 
	@${RM} ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/2138657381/SD_FAT.o   ../../HedgeHog/SD_FAT.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o 
	
${OBJECTDIR}/_ext/1472/osc.o: ../osc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/osc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/osc.o   ../osc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/osc.o 
	
${OBJECTDIR}/_ext/1360904562/rtcc.o: ../RTC/rtcc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1360904562 
	@${RM} ${OBJECTDIR}/_ext/1360904562/rtcc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1360904562/rtcc.o   ../RTC/rtcc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1360904562/rtcc.o 
	
${OBJECTDIR}/_ext/1472/usb_descriptors.o: ../usb_descriptors.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/usb_descriptors.o   ../usb_descriptors.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/usb_descriptors.o 
	
${OBJECTDIR}/_ext/1472/config_cdc.o: ../config_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/config_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/config_cdc.o   ../config_cdc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/config_cdc.o 
	
${OBJECTDIR}/_ext/1472/HHG_conf.o: ../HHG_conf.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/HHG_conf.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/HHG_conf.o   ../HHG_conf.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/HHG_conf.o 
	
${OBJECTDIR}/_ext/1472/SD_Buffer.o: ../SD_Buffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/SD_Buffer.o   ../SD_Buffer.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/SD_Buffer.o 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_TESTBED -DRAW_SAMPLING -I"/opt/microchip/Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/main.o   ../main.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/main.o 
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_LD} $(MP_EXTRA_LD_PRE) "../rm18f46j50_g.lkr"  -p$(MP_PROCESSOR_OPTION_LD)  -w -x -u_DEBUG -l"/opt/microchip/mplabc18/v3.40/lib"  -z__MPLAB_BUILD=1  -u_CRUNTIME -z__MPLAB_DEBUG=1 $(MP_LINKER_DEBUG_OPTION) -l ${MP_CC_DIR}/../lib  -o dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}   
else
dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_LD} $(MP_EXTRA_LD_PRE) "../rm18f46j50_g.lkr"  -p$(MP_PROCESSOR_OPTION_LD)  -w  -l"/opt/microchip/mplabc18/v3.40/lib"  -z__MPLAB_BUILD=1  -u_CRUNTIME -l ${MP_CC_DIR}/../lib  -o dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}   
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r build/raw_sampling_testbed
	${RM} -r dist/raw_sampling_testbed

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell "${PATH_TO_IDE_BIN}"mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
