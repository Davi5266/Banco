import sqlite3
class database:
	def __init__(self):
		self.conn = sqlite3.connect('projetoinfo.db')
		self.cur = self.conn.cursor()

		data_user = '''
			CREATE TABLE IF NOT EXISTS usuarios(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			num_conta TEXT VARCHAR(30),
			nome TEXT VARCHAR(30),
			saldo INTEGER DEFAULT 1000);
		'''

		history_user = '''
			CREATE TABLE IF NOT EXISTS historico(
			history_id INTEGER PRIMARY KEY AUTOINCREMENT,
			num_conta INTEGER,
			atividade TEXT NOT NULL,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (num_conta) REFERENCES usuarios (num_conta)
			);
		'''
		self.conn.execute(data_user)
		self.conn.execute(history_user)
		self.conn.commit()


	def add_user(self):
		num_conta = input('Número da Conta: ')
		nome = input('Nome: ')
		atividade = 'Conta ativada'
		saldo = 1000
		self.cur.execute("INSERT INTO usuarios(num_conta,nome,saldo) VALUES('"+num_conta+"','"+nome+"','"+str(saldo)+"');")
		self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+num_conta+"','"+atividade+"')")
		self.conn.commit()

	def user_saldo(self):
		atividade = "Consulta de saldo."
		usuario = input("Digite o nome do usuario para consultar o saldo: ")
		self.cur.execute("SELECT nome, saldo FROM usuarios WHERE num_conta='"+usuario+"';")
		saldo = self.cur.fetchone()
		if saldo:
			print("Nome: {}\nSaldo: R$ {}".format(saldo[0],saldo[1]))
			self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+usuario+"','"+atividade+"')")
			self.conn.commit()
		else:
			print("Conta não encontrada!")

	def saque(self):
		usuario = input("Número da conta: ")
		self.cur.execute("SELECT nome, saldo FROM usuarios WHERE num_conta='"+usuario+"';")
		saldo = self.cur.fetchone()
		if saldo:
			valor = int(input("Digite o valor para efetuar o saque: "))
			if valor < int(saldo[1]):
				atividade = "Saque no valor de R$ {}.".format(valor)
				valor = int(saldo[1]) - valor
				self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+usuario+"','"+atividade+"')")
				self.cur.execute("UPDATE usuarios SET saldo='"+str(valor)+"' WHERE num_conta='"+usuario+"';")
				self.conn.commit()
				self.cur.execute("SELECT saldo FROM usuarios WHERE num_conta='"+usuario+"';")
				print("Saldo atual: R$ {}".format(self.cur.fetchone()[0]))
			else:
				print("Saldo insuficiente!")
		else:
			print("Conta não encontrada!")

	def deposita(self):
		conta = input('Digite o numero da conta para deposito: ')
		usuario = self.cur.execute("SELECT num_conta,nome,saldo FROM usuarios WHERE num_conta='"+conta+"';")
		if usuario:
			print(self.cur.fetchone())

			saldo = self.cur.execute("SELECT saldo FROM usuarios WHERE num_conta='"+conta+"';")
			saldo = saldo.fetchone()
			for i in saldo:
				saldo = i

			valor = int(input('Digite o valor para depositar: '))
			atividade = "Deposito de R$ {}".format(valor)
			valor = valor + saldo
			self.cur.execute("UPDATE usuarios SET saldo='"+str(valor)+"' WHERE num_conta='"+conta+"';")
			self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+conta+"','"+atividade+"')")

			self.conn.commit()

		else:
			print('Usuario não encontrado!')

	def historico(self):
		print("HISTORICO")
		usuario = int(input("Digite o numero da conta: "))
		self.cur.execute("SELECT atividade, timestamp FROM historico WHERE num_conta='"+str(usuario)+"';")
		historico = self.cur.fetchall()
		if historico:
			for i in historico:
				print("Atividade: {} Data hora: {}".format(i[0],i[1]))
		else:
			print("Usuário Inválido!")

	def transfere(self):
		print("TRANSFERENCIA")
		conta_01 = input("Conta para realizar a transferência: ")
		self.cur.execute("SELECT num_conta, nome, saldo FROM usuarios WHERE num_conta='"+conta_01+"';")
		conta_01 = self.cur.fetchone()
		conta_02 = input("Conta de destino: ")
		self.cur.execute("SELECT num_conta, nome, saldo FROM usuarios WHERE num_conta='"+conta_02+"';")
		conta_02 = self.cur.fetchone()
		if conta_01:
			if conta_02:
				valor = int(input("Digite o valor para realizar a transferência: "))
				if valor < int(conta_01[2]):
					atividade = "Transferência de R${} para {}".format(valor,conta_02[1])

					transf = int(conta_01[0]) - valor
					valor = valor + int(conta_02[2])
					self.cur.execute("UPDATE usuarios SET saldo='"+str(valor)+"' WHERE num_conta='"+conta_02[0]+"';")
					self.cur.execute("UPDATE usuarios SET saldo='"+str(transf)+"'  WHERE num_conta='"+conta_01[0]+"' ;")

					atividade_02 = "Recebeu transferência de R${} de {}".format(valor,conta_01[1])

					self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+conta_01[0]+"','"+atividade+"')")
					self.cur.execute("INSERT INTO historico(num_conta,atividade) VALUES ('"+conta_02[0]+"','"+atividade_02+"')")


					self.conn.commit()
				else:
					print('Saldo insuficiênte!')
			else:
				print('Conta de destino inválida!')
		else:
			print('Conta de tranferência inválida!')
