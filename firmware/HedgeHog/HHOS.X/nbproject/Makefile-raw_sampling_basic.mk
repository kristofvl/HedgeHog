#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
include Makefile

# Environment
# Adding MPLAB X bin directory to path
PATH:=/opt/microchip/mplabx/mplab_ide/mplab_ide/modules/../../bin/:$(PATH)
MKDIR=mkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=raw_sampling_basic
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
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/1134515050/ADXL345.o ${OBJECTDIR}/_ext/677419432/ambient_light.o ${OBJECTDIR}/_ext/2138657381/SD_FAT.o ${OBJECTDIR}/_ext/1472/osc.o ${OBJECTDIR}/_ext/1360904562/rtcc.o ${OBJECTDIR}/_ext/1472/usb_descriptors.o ${OBJECTDIR}/_ext/1472/config_cdc.o ${OBJECTDIR}/_ext/1472/HHG_conf.o ${OBJECTDIR}/_ext/1472/SD_Buffer.o ${OBJECTDIR}/_ext/1472/main.o ${OBJECTDIR}/_ext/926206843/usb_device.o ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o ${OBJECTDIR}/_ext/123996954/usb_function_msd.o ${OBJECTDIR}/_ext/491339551/SD-SPI.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/1134515050/ADXL345.o.d ${OBJECTDIR}/_ext/677419432/ambient_light.o.d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d ${OBJECTDIR}/_ext/1472/osc.o.d ${OBJECTDIR}/_ext/1360904562/rtcc.o.d ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d ${OBJECTDIR}/_ext/1472/config_cdc.o.d ${OBJECTDIR}/_ext/1472/HHG_conf.o.d ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d ${OBJECTDIR}/_ext/1472/main.o.d ${OBJECTDIR}/_ext/926206843/usb_device.o.d ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o.d ${OBJECTDIR}/_ext/123996954/usb_function_msd.o.d ${OBJECTDIR}/_ext/491339551/SD-SPI.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/1134515050/ADXL345.o ${OBJECTDIR}/_ext/677419432/ambient_light.o ${OBJECTDIR}/_ext/2138657381/SD_FAT.o ${OBJECTDIR}/_ext/1472/osc.o ${OBJECTDIR}/_ext/1360904562/rtcc.o ${OBJECTDIR}/_ext/1472/usb_descriptors.o ${OBJECTDIR}/_ext/1472/config_cdc.o ${OBJECTDIR}/_ext/1472/HHG_conf.o ${OBJECTDIR}/_ext/1472/SD_Buffer.o ${OBJECTDIR}/_ext/1472/main.o ${OBJECTDIR}/_ext/926206843/usb_device.o ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o ${OBJECTDIR}/_ext/123996954/usb_function_msd.o ${OBJECTDIR}/_ext/491339551/SD-SPI.o


CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

# Path to java used to run MPLAB X when this makefile was created
MP_JAVA_PATH="/usr/lib/jvm/java-6-sun-1.6.0.26/jre/bin/"
OS_CURRENT="$(shell uname -s)"
############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
MP_CC="/opt/microchip/mplabc18/v3.40/bin/mcc18"
# MP_BC is not defined
MP_AS="/opt/microchip/mplabc18/v3.40/bin/../mpasm/MPASMWIN"
MP_LD="/opt/microchip/mplabc18/v3.40/bin/mplink"
MP_AR="/opt/microchip/mplabc18/v3.40/bin/mplib"
DEP_GEN=${MP_JAVA_PATH}java -jar "/opt/microchip/mplabx/mplab_ide/mplab_ide/modules/../../bin/extractobjectdependencies.jar" 
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps
MP_CC_DIR="/opt/microchip/mplabc18/v3.40/bin"
# MP_BC_DIR is not defined
MP_AS_DIR="/opt/microchip/mplabc18/v3.40/bin/../mpasm"
MP_LD_DIR="/opt/microchip/mplabc18/v3.40/bin"
MP_AR_DIR="/opt/microchip/mplabc18/v3.40/bin"
# MP_BC_DIR is not defined

.build-conf:  ${BUILD_SUBPROJECTS}
	${MAKE}  -f nbproject/Makefile-raw_sampling_basic.mk dist/${CND_CONF}/${IMAGE_TYPE}/HHOS.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

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
${OBJECTDIR}/_ext/1134515050/ADXL345.o: ../ADXL345driver/ADXL345.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1134515050 
	@${RM} ${OBJECTDIR}/_ext/1134515050/ADXL345.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1134515050/ADXL345.o   ../ADXL345driver/ADXL345.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1134515050/ADXL345.o 
	
${OBJECTDIR}/_ext/677419432/ambient_light.o: ../ambient_light\ driver/ambient_light.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/677419432 
	@${RM} ${OBJECTDIR}/_ext/677419432/ambient_light.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/677419432/ambient_light.o   "../ambient_light driver/ambient_light.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/677419432/ambient_light.o 
	
${OBJECTDIR}/_ext/2138657381/SD_FAT.o: ../../HedgeHog/SD_FAT.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/2138657381 
	@${RM} ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/2138657381/SD_FAT.o   ../../HedgeHog/SD_FAT.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o 
	
${OBJECTDIR}/_ext/1472/osc.o: ../osc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/osc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/osc.o   ../osc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/osc.o 
	
${OBJECTDIR}/_ext/1360904562/rtcc.o: ../RTC/rtcc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1360904562 
	@${RM} ${OBJECTDIR}/_ext/1360904562/rtcc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1360904562/rtcc.o   ../RTC/rtcc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1360904562/rtcc.o 
	
${OBJECTDIR}/_ext/1472/usb_descriptors.o: ../usb_descriptors.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/usb_descriptors.o   ../usb_descriptors.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/usb_descriptors.o 
	
${OBJECTDIR}/_ext/1472/config_cdc.o: ../config_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/config_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/config_cdc.o   ../config_cdc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/config_cdc.o 
	
${OBJECTDIR}/_ext/1472/HHG_conf.o: ../HHG_conf.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/HHG_conf.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/HHG_conf.o   ../HHG_conf.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/HHG_conf.o 
	
${OBJECTDIR}/_ext/1472/SD_Buffer.o: ../SD_Buffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/SD_Buffer.o   ../SD_Buffer.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/SD_Buffer.o 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/main.o   ../main.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/main.o 
	
${OBJECTDIR}/_ext/926206843/usb_device.o: ../../../../Microchip/USB/usb_device.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/926206843 
	@${RM} ${OBJECTDIR}/_ext/926206843/usb_device.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/926206843/usb_device.o   ../../../../Microchip/USB/usb_device.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/926206843/usb_device.o 
	
${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o: ../../../../Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1083301514 
	@${RM} ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o   "../../../../Microchip/USB/CDC Device Driver/usb_function_cdc.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o 
	
${OBJECTDIR}/_ext/123996954/usb_function_msd.o: ../../../../Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/123996954 
	@${RM} ${OBJECTDIR}/_ext/123996954/usb_function_msd.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/123996954/usb_function_msd.o   "../../../../Microchip/USB/MSD Device Driver/usb_function_msd.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/123996954/usb_function_msd.o 
	
${OBJECTDIR}/_ext/491339551/SD-SPI.o: ../../../../Microchip/MDD\ File\ System/SD-SPI.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/491339551 
	@${RM} ${OBJECTDIR}/_ext/491339551/SD-SPI.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -D__DEBUG  -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/491339551/SD-SPI.o   "../../../../Microchip/MDD File System/SD-SPI.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/491339551/SD-SPI.o 
	
else
${OBJECTDIR}/_ext/1134515050/ADXL345.o: ../ADXL345driver/ADXL345.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1134515050 
	@${RM} ${OBJECTDIR}/_ext/1134515050/ADXL345.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1134515050/ADXL345.o   ../ADXL345driver/ADXL345.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1134515050/ADXL345.o 
	
${OBJECTDIR}/_ext/677419432/ambient_light.o: ../ambient_light\ driver/ambient_light.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/677419432 
	@${RM} ${OBJECTDIR}/_ext/677419432/ambient_light.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/677419432/ambient_light.o   "../ambient_light driver/ambient_light.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/677419432/ambient_light.o 
	
${OBJECTDIR}/_ext/2138657381/SD_FAT.o: ../../HedgeHog/SD_FAT.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/2138657381 
	@${RM} ${OBJECTDIR}/_ext/2138657381/SD_FAT.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/2138657381/SD_FAT.o   ../../HedgeHog/SD_FAT.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/2138657381/SD_FAT.o 
	
${OBJECTDIR}/_ext/1472/osc.o: ../osc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/osc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/osc.o   ../osc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/osc.o 
	
${OBJECTDIR}/_ext/1360904562/rtcc.o: ../RTC/rtcc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1360904562 
	@${RM} ${OBJECTDIR}/_ext/1360904562/rtcc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1360904562/rtcc.o   ../RTC/rtcc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1360904562/rtcc.o 
	
${OBJECTDIR}/_ext/1472/usb_descriptors.o: ../usb_descriptors.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/usb_descriptors.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/usb_descriptors.o   ../usb_descriptors.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/usb_descriptors.o 
	
${OBJECTDIR}/_ext/1472/config_cdc.o: ../config_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/config_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/config_cdc.o   ../config_cdc.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/config_cdc.o 
	
${OBJECTDIR}/_ext/1472/HHG_conf.o: ../HHG_conf.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/HHG_conf.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/HHG_conf.o   ../HHG_conf.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/HHG_conf.o 
	
${OBJECTDIR}/_ext/1472/SD_Buffer.o: ../SD_Buffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/SD_Buffer.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/SD_Buffer.o   ../SD_Buffer.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/SD_Buffer.o 
	
${OBJECTDIR}/_ext/1472/main.o: ../main.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1472 
	@${RM} ${OBJECTDIR}/_ext/1472/main.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1472/main.o   ../main.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1472/main.o 
	
${OBJECTDIR}/_ext/926206843/usb_device.o: ../../../../Microchip/USB/usb_device.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/926206843 
	@${RM} ${OBJECTDIR}/_ext/926206843/usb_device.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/926206843/usb_device.o   ../../../../Microchip/USB/usb_device.c 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/926206843/usb_device.o 
	
${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o: ../../../../Microchip/USB/CDC\ Device\ Driver/usb_function_cdc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/1083301514 
	@${RM} ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o   "../../../../Microchip/USB/CDC Device Driver/usb_function_cdc.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/1083301514/usb_function_cdc.o 
	
${OBJECTDIR}/_ext/123996954/usb_function_msd.o: ../../../../Microchip/USB/MSD\ Device\ Driver/usb_function_msd.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/123996954 
	@${RM} ${OBJECTDIR}/_ext/123996954/usb_function_msd.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/123996954/usb_function_msd.o   "../../../../Microchip/USB/MSD Device Driver/usb_function_msd.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/123996954/usb_function_msd.o 
	
${OBJECTDIR}/_ext/491339551/SD-SPI.o: ../../../../Microchip/MDD\ File\ System/SD-SPI.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} ${OBJECTDIR}/_ext/491339551 
	@${RM} ${OBJECTDIR}/_ext/491339551/SD-SPI.o.d 
	${MP_CC} $(MP_EXTRA_CC_PRE) -p$(MP_PROCESSOR_OPTION) -DHEDGEHOG_BASIC -DRAW_SAMPLING -I"../../../../Microchip/Include" -I"../BMA150 driver" -I"../ADXL345driver" -I"../Soft Start" -I"../RTC" -I"../OLED driver" -I"../" -mL  -I ${MP_CC_DIR}/../h  -fo ${OBJECTDIR}/_ext/491339551/SD-SPI.o   "../../../../Microchip/MDD File System/SD-SPI.c" 
	@${DEP_GEN} -d ${OBJECTDIR}/_ext/491339551/SD-SPI.o 
	
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

# Clean Targets
.clean-conf:
	${RM} -r build/raw_sampling_basic
	${RM} -r dist/raw_sampling_basic

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell "/opt/microchip/mplabx/mplab_ide/mplab_ide/modules/../../bin/"mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
