# Caterpillar_hack
Vehicle Maintenance Optimization Project
Features
1. Precautionary Alerts
This feature analyzes vehicle data to assess the probability of component failures. It provides insights into which parts of a vehicle are most likely to encounter issues and suggests best practices to prevent these problems. The output includes a visual plot comparing vehicle types against the probability of each part failing, making it easier to identify sensitive parts and their potential causes.

2. Intelligent Work Planner
This feature helps users plan their work schedule efficiently. By inputting the number of assets, deadlines, weather conditions, and type of work, the system generates an optimized work plan to minimize the risk of breakdowns. Deadlines are categorized into Critical, Hard, and Soft:

Critical: The system ensures deadlines are met, recommending advance orders for spare parts and equipment.
Hard: Allows for a maximum 5-day extension, with recommendations for spare parts and equipment after the extension period.
Soft: If failure probability exceeds 50%, the system advises extending the deadline to keep downtime under 30%.
3. Daily Diagnosis
This feature provides daily workload recommendations for each asset based on the day's weather, backlog, machine name, initial KPIs, and assigned tasks. It assesses the impact of the recommended workload on the overall plan and suggests additional machinery or order times if a critical deadline is at risk.

