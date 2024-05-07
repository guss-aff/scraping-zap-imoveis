import re

text = "R$ 1600/mêsCond R$ 440 | IPTU R$ 100 (vencimento: 10/02/2024)"

# Extraindo o período de pagamento do aluguel
periodo_aluguel = re.findall(r"(\/\w+)", text)[0]

# Extraindo o período de pagamento do IPTU
# periodo_iptu = re.findall(r"(?<=vencimento: )\d+/\d+/\d+", text)[0]

print(f"Período de pagamento do aluguel: {periodo_aluguel}")
# print(f"Período de pagamento do IPTU: {periodo_iptu}")

