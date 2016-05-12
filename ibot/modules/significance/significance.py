from ibot.modules.base_module import BaseIBotModule






class IBotModule(BaseIBotModule):

	def __init__(self):
		super(IBotModule,self).__init__(
						name='Significance Charts', 
						anchor='significance',
						info='Make volcano and MA charts')

		self.intro += """
						<p>
						Volcano and MA charts. These charts show points which are prominent and merit further investigation.
						Click and drag to select an area to zoom in.
						</p>
						"""

	def strictness(self, strict):
		if strict == 0:
			minLfc=0.5
			maxApv=0.1
			rarefier=0.1
		elif strict == 1:
			minLfc=0.75
			maxApv=0.05
			rarefier=0.05
		elif strict == 2:
			minLfc=1
			maxApv=0.01
			rarefier=0.01
		else:
			minLfc=1
			maxApv=0.001
			rarefier=0.005
		return minLfc, maxApv, rarefier

	def buildChartSet(self, name, table, idcol='ids',groups=None,strict=1):

		minLfc, maxApv, rarefier = self.strictness(strict)
		if groups == None:
			assert len(groups) == 2
			v = volcanoMultiGroup(table,name,idcol,minLfc,maxApv,rarefier)
			m = maMultiGroup(table,name,idcol,minLfc,maxApv,rarefier)
		else:
			v = volcano(table,groups,idcol,minLfc,maxApv,rarefier)
			m = ma(table,groups,idcol,minLfc,maxApv,rarefier)

		plot = self.split_over_columns([[v,m]],rowwise=True)

		self.sections.append({
			'name' : name,
			'anchor' : 'sig_plots_{}'.format(name),
			'content' : plot
			})



def volcano(table,groups,idcol,minLfc,maxApv,rarefier):
	cols, rows = table.getTable(sqlCmd="SELECT {}, logFC, adj_P_Val FROM {{table_name}} ".format(idcol))

	lava = {'not significant (rarefied)':[], 'significant':[]}
	for gene, lfc, apv in rows:
		if abs(lfc) > minLfc and apv < maxApv:
			lava['significant'].append({'name':gene, 'x':lfc, 'y':-math.log(apv,2)})
		elif random() <  rarefier: # rarify insignificant points so page loads faster 
			lava['not significant (rarefied)'].append([lfc,-math.log(apv,2)])

	return scatter.plot(lava, pconfig={
										'ylab':'Negative log of adjusted p value', 
										'xlab':'average log fold change', 
										'title':'Volcano Plot {} v. {}'.format(*groups),
										'legend':True
										})

def ma(table,groups,minLfc,maxApv,rarefier):
	cols, rows = table.getTable(sqlCmd="SELECT {}, logFC, adj_P_Val, AveExpr FROM {{table_name}} ".format(idcol))

	lava = {'not significant (rarefied)':[], 'significant':[]}
	for  gene, lfc, apv, aE in rows:
		if abs(lfc) > minLfc and apv < maxApv:
			lava['significant'].append({'name':gene, 'y':lfc, 'x':aE})
		elif random() <  rarefier: # rarify insignificant points so page loads faster 
			lava['not significant (rarefied)'].append([aE,lfc])

	return scatter.plot(lava, pconfig={
										'ylab':'Ave. Log Fold Change', 
										'xlab':'Ave. Expression', 
										'title':'MA Plot {} v. {}'.format(*groups),
										'legend':True
										})

def volcanoMultiGroup(table,name,minLfc,maxApv,rarefier):
	cols, rows = table.getTable(sqlCmd="SELECT {}, logFC, adj_P_Val, group1, group2 FROM {{table_name}} ".format(idcol))


	lava = {'not significant (rarefied)':[]}
	for taxa, lfc, apv, g1, g2 in rows:
		group = "{} {}".format(g1,g2)
		if abs(lfc) > minLfc and apv < maxApv:
			if group not in lava:
				lava[group] = []
			lava[group].append({'name':taxa, 'x':lfc, 'y':-math.log(apv,2)})
		elif random() <  rarefier: # rarify insignificant points so page loads faster 
			lava['not significant (rarefied)'].append([lfc,-math.log(apv,2)])

	return scatter.plot(lava, pconfig={
										'ylab':'Negative log of adjusted p value', 
										'xlab':'average log fold change', 
										'title':'{} Volcano Plot'.format(name),
										'legend':True
										})

def maMultiGroup(table,taxaLvl,minLfc,maxApv,rarefier):
	cols, rows = table.getTable(sqlCmd="SELECT {}, logFC, adj_P_Val, AveExpr, group1, group2 FROM {{table_name}} ".format(idcol))

	lava = {'not significant (rarefied)':[]}
	for  taxa, lfc, apv, aE, g1, g2 in rows:
		group = "{} {}".format(g1,g2)
		if abs(lfc) > minLfc and apv < maxApv:
			if group not in lava:
				lava[group] = []
			lava[group].append({'name':taxa, 'y':lfc, 'x':aE})
		elif random() <  rarefier: # rarify insignificant points so page loads faster 
			lava['not significant (rarefied)'].append([aE,lfc])

	return scatter.plot(lava, pconfig={
										'ylab':'Ave. Log Fold Change', 
										'xlab':'Ave. Expression', 
										'title':'{} MA Plot'.format(taxaLvl),
										'legend':True
										})