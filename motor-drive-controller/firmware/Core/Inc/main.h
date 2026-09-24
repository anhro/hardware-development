/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define OSC_IN_Pin GPIO_PIN_0
#define OSC_IN_GPIO_Port GPIOH
#define OSC_OUT_Pin GPIO_PIN_1
#define OSC_OUT_GPIO_Port GPIOH
#define TEMP_SENSE_Pin GPIO_PIN_0
#define TEMP_SENSE_GPIO_Port GPIOC
#define ISENSE_SO1_Pin GPIO_PIN_0
#define ISENSE_SO1_GPIO_Port GPIOA
#define ISENSE_SO2_Pin GPIO_PIN_1
#define ISENSE_SO2_GPIO_Port GPIOA
#define ISENSE_SO3_Pin GPIO_PIN_2
#define ISENSE_SO3_GPIO_Port GPIOA
#define DRV_nSCS_Pin GPIO_PIN_4
#define DRV_nSCS_GPIO_Port GPIOA
#define DRV_SCLK_Pin GPIO_PIN_5
#define DRV_SCLK_GPIO_Port GPIOA
#define DRV_SDO_Pin GPIO_PIN_6
#define DRV_SDO_GPIO_Port GPIOA
#define DRV_INLA_Pin GPIO_PIN_7
#define DRV_INLA_GPIO_Port GPIOA
#define DRV_nFAULT_Pin GPIO_PIN_4
#define DRV_nFAULT_GPIO_Port GPIOC
#define DRV_PWRGD_Pin GPIO_PIN_5
#define DRV_PWRGD_GPIO_Port GPIOC
#define DRV_INLB_Pin GPIO_PIN_0
#define DRV_INLB_GPIO_Port GPIOB
#define DRV_INLC_Pin GPIO_PIN_1
#define DRV_INLC_GPIO_Port GPIOB
#define HALL1_Pin GPIO_PIN_6
#define HALL1_GPIO_Port GPIOC
#define HALL2_Pin GPIO_PIN_7
#define HALL2_GPIO_Port GPIOC
#define HALL3_Pin GPIO_PIN_8
#define HALL3_GPIO_Port GPIOC
#define DRV_INHA_Pin GPIO_PIN_8
#define DRV_INHA_GPIO_Port GPIOA
#define DRV_INHB_Pin GPIO_PIN_9
#define DRV_INHB_GPIO_Port GPIOA
#define DRV_INHC_Pin GPIO_PIN_10
#define DRV_INHC_GPIO_Port GPIOA
#define JTMS_Pin GPIO_PIN_13
#define JTMS_GPIO_Port GPIOA
#define JTCK_Pin GPIO_PIN_14
#define JTCK_GPIO_Port GPIOA
#define JTDI_Pin GPIO_PIN_15
#define JTDI_GPIO_Port GPIOA
#define JTDO_Pin GPIO_PIN_3
#define JTDO_GPIO_Port GPIOB
#define NJTRST_Pin GPIO_PIN_4
#define NJTRST_GPIO_Port GPIOB
#define DRV_SDI_Pin GPIO_PIN_5
#define DRV_SDI_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
