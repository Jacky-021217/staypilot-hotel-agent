# 星澜酒店（虚构）服务知识库 | StayPilot Demo Hotel Policies

> 重要：以下内容均为演示用途的**模拟政策**，不属于任何真实酒店。模型回答必须基于本文档，不得臆测。
> **Important:** This is a fictional demo hotel. All policies below are synthetic and for demonstration only. They must not be presented as the policies of a real hotel. The AI must base its answers on this document and must not invent information.

## 酒店基本信息 / General
- 酒店名称：星澜酒店（演示酒店） / **Hotel name:** Xinglan Demo Hotel (fictional).
- 前台：全天 24 小时服务 / **Front desk:** Available 24 hours a day.
- 酒店住客服务热线：请通过前台或酒店官方应用内服务入口联系，本文档不提供真实电话。 / **Guest assistance:** Please contact the front desk or use the service section of the hotel's official app. No real phone number is provided in this document.

## 入住与退房 / Check-in & Check-out
- 标准入住：14:00 起 / **Standard check-in:** From 14:00 (2:00 PM).
- 标准退房：12:00 前 / **Standard check-out:** Before 12:00 (noon).
- 延迟退房：可提出申请，需前台确认房态及可能产生的费用；AI 不得承诺一定可延迟或免收费。 / **Late check-out:** Guests may request a late check-out, subject to room availability and possible charges confirmed by the front desk. The AI must not guarantee approval or a fee waiver.
- 提前入住：视房态，由前台确认；AI 不得直接保证。 / **Early check-in:** Subject to room availability and confirmation by the front desk. The AI must not guarantee early check-in.

## 餐饮 / Dining
- 早餐时间：06:30–10:00 / **Breakfast hours:** 06:30–10:00 (6:30–10:00 AM).
- 早餐地点：酒店二层餐厅 / **Breakfast location:** Restaurant on Level 2.
- 早餐是否包含在订单内：取决于具体预订方案，请住客查看订单详情或询问前台；AI 无法访问实际订单。 / **Breakfast inclusion:** Whether breakfast is included depends on the guest's booking plan. Guests should check their reservation details or ask the front desk. The AI cannot access actual reservations.

## 客房服务 / Room Service
- 饮用水、毛巾、额外枕头等物品可提交服务请求，由客房服务部处理。 / **Available requests:** Guests may request drinking water, towels, extra pillows, and similar items. Requests are handled by housekeeping.
- 接单后不保证具体送达时间，需以酒店员工确认信息为准。 / **Delivery time:** No specific delivery time is guaranteed after a request is accepted. Guests should rely on confirmation from hotel staff.
- 创建服务工单前，需确认房号、物品、数量并获得住客明确同意。 / **Before submitting a service ticket:** Confirm the room number, requested item(s), and quantity, and obtain the guest's explicit consent.

## 设施维护 / Maintenance
- 空调、照明、浴室设备等故障可提交工程维修请求。 / **Maintenance requests:** Guests may report problems with air conditioning, lighting, bathroom fixtures, and similar facilities for the maintenance team.
- 须获取房号、故障描述及明确的提交确认。 / **Before submitting a maintenance ticket:** Obtain the room number, a description of the issue, and the guest's explicit confirmation to submit the request.
- 如果出现烟雾、火灾、严重漏水、人身伤害等紧急情况，应优先提示住客联系酒店前台及当地紧急服务，不得只创建普通维修工单。 / **Emergencies:** In cases of smoke, fire, serious water leaks, personal injury, or similar emergencies, advise the guest to contact the front desk and local emergency services immediately. Do not handle these cases solely by creating a routine maintenance ticket.

## Wi-Fi / Network
- 酒店提供公共区域和客房 Wi-Fi。 / **Wi-Fi availability:** Wi-Fi is available in public areas and guest rooms.
- 连接方式与登录凭据请查看客房内实际指引或联系前台；AI 不得编造密码。 / **Connection instructions:** Guests should check the instructions provided in their room or contact the front desk for login details. The AI must not invent a Wi-Fi password.

## 停车 / Parking
- 是否有空车位及收费标准，需由前台实时确认；本知识库不提供实时停车状态。 / **Parking availability and fees:** Guests must confirm available parking spaces and applicable charges with the front desk. This knowledge base does not provide real-time parking information.

## 投诉与人工协助 / Complaints & Human Assistance
- 噪声、卫生及服务体验问题可记录为投诉并转交前台主管。 / **Complaints:** Issues relating to noise, cleanliness, or service experience may be recorded as complaints and forwarded to the front desk supervisor.
- 涉及安全、医疗、财物丢失或隐私敏感的情况，应提供人工处理建议，不自动做承诺或赔偿决定。 / **Sensitive cases:** For safety concerns, medical issues, lost property, or privacy-sensitive matters, recommend assistance from hotel staff. The AI must not make commitments or compensation decisions automatically.

## 多语言 / Languages
- 可使用中文或英文提出酒店咨询与服务需求。 / **Supported languages:** Guests may ask questions and submit service requests in Chinese or English.
- Agent 应以住客所使用语言回答，工单内部字段用标准英文枚举。 / **Response and ticket language:** The Agent should respond in the same language used by the guest. Internal ticket fields should use standardized English enumerated values.

## AI 执行约束 / AI Operating Rules
- 未查询到的收费、可用性、时间、预约详情不能编造。 / **No fabricated information:** Do not invent fees, availability, timings, or booking details that have not been verified.
- 不查询或暴露其他住客信息。 / **Guest privacy:** Do not access or disclose other guests' information.
- 未经明确授权不得自动取消、扣款、退款或修改预订。 / **Authorization required:** Do not automatically cancel reservations, charge payments, issue refunds, or change bookings without explicit authorization.
- 工单接口失败时只能说“提交失败”，不能假称成功。 / **Ticket submission failures:** If the ticket API fails, inform the guest that the request could not be submitted. Never claim the submission succeeded.
