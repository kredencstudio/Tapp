"""
name : gf_curveOnMeshCtx.py

author : Guillaume FERRACHAT

launch :
import gf_curveOnMeshCtx as cmCtx
reload(cmCtx)

cmCtx.UI().create()

usage :
Select mesh(es), run the script, choose the precision and click the button
"""

import maya.cmds as cmds

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import math as math

class meshDrawCtx():
	"""
	Tool class
	"""
	def __init__(self, targetObj = [], step = 0.25, mesh = False, bRad = 1, bMult = 1, taper = 1, tMult = .1,autoAdd=True):
		"""
		initialize tool
		"""
		# create dragger context
		self.dragCtx = "gf_meshPlace_draggerCtx"
		if (cmds.draggerContext(self.dragCtx, exists=True)):
			cmds.deleteUI(self.dragCtx)
		cmds.draggerContext(self.dragCtx, pressCommand=self.onPress, dragCommand=self.onDrag, releaseCommand=self.onRelease, name=self.dragCtx, cursor='crossHair', undoMode='step')
		
		self.targetObj = targetObj		# objects list
		self.worldUp = om.MVector(0,-1,0)
		self.step = step
		self.mesh = mesh
		self.bRad = bRad
		self.bMult = bMult
		self.taper = taper
		self.tMult = tMult
		self.autoAdd = autoAdd
	def run(self):
		"""
		set current tool
		"""
		if (cmds.draggerContext(self.dragCtx, exists=True)):
			cmds.setToolTo(self.dragCtx)
			
	def onPress(self):
		"""
		execute on press
		"""
		# modifier
		self.mod = cmds.getModifiers()
		
		# button
		self.btn = cmds.draggerContext(self.dragCtx, query=True, button=True)
		
		# timer
		self.timer = cmds.timerX()
		initPos = cmds.draggerContext(self.dragCtx, query=True, anchorPoint=True)
		
		# camera far clip
		currentView = omui.M3dView().active3dView()
		camDP = om.MDagPath()
		
		currentView.getCamera(camDP)
		camFn = om.MFnCamera(camDP)
		farclip = camFn.farClippingPlane()
		
		# screen to world conversion
		worldPos, worldDir = utils().viewToWorld(initPos[0],initPos[1])
		
		if self.btn is not 2:
			closestHit = None
			closestObj = None
			for obj in self.targetObj:
				if cmds.objExists(obj):
					state, hit, fnMesh, facePtr, triPtr = utils().intersect(obj, worldPos, worldDir, farclip)
					
					if state is True:
						dif = [hit.x - worldPos[0],hit.y - worldPos[1],hit.z - worldPos[2]]
						distToCam = math.sqrt(math.pow(float(dif[0]),2) + math.pow(float(dif[1]),2) + math.pow(float(dif[2]),2))
						if closestHit == None:
							closestHit = distToCam
							closestObj = [state, hit, fnMesh, facePtr, triPtr]
						elif distToCam < closestHit:
							closestHit = distToCam
							closestObj = [state, hit, fnMesh, facePtr, triPtr]
				else:
					self.targetObj.remove(obj)
			if closestObj is not None:
				state, hit, fnMesh, facePtr, triPtr = closestObj
				
				mHit = om.MPoint(hit)
				# get smooth normal
				normal = om.MVector()
				fnMesh.getClosestNormal(mHit, normal, om.MSpace.kWorld, None)
				
				# get smooth normal
				normal = om.MVector()
				fnMesh.getClosestNormal(mHit, normal, om.MSpace.kWorld, None)
				
				tangent = utils().crossProduct(normal,self.worldUp)
				
				upAxis = utils().crossProduct(normal,tangent)
				
				# define transformation matrix
				matrix = [tangent.x,tangent.y,tangent.z,0,upAxis.x,upAxis.y,upAxis.z,0,normal.x,normal.y,normal.z,0,hit.x,hit.y,hit.z,0]
				
				# create object
				if self.mod == 0:
					self.loc = cmds.curve(p = (hit.x,hit.y,hit.z))
				# cmds.toggle(self.loc, localAxis=True)
				
				# store values
				self.prevHit = hit
				print self.prevHit
				
				self.screenPoint = initPos
				
				self.angle = 0
				
				# draw Mesh
				if self.mesh is True and self.mod == 0:
					self.circle = cmds.circle(center = (hit.x,hit.y,hit.z),radius = self.bRad,d=3)
					self.extrude = cmds.extrude(self.circle[0],self.loc,po=1, ch=True,rn=False,et=2,ucp=0,fpt=0,upn=0,rotation=0,scale=1,rsp=1)
					self.nbTes = cmds.listConnections(self.extrude[1] + '.outputSurface')[0]
					
					cmds.setAttr(self.nbTes + '.polygonType',1)
					cmds.setAttr(self.nbTes + '.format',2)
					cmds.setAttr(self.nbTes + '.polygonCount',200)
					cmds.setAttr(self.nbTes + '.uType',3)
					cmds.setAttr(self.nbTes + '.uNumber',1)
					cmds.setAttr(self.nbTes + '.vType',3)
					cmds.setAttr(self.nbTes + '.vNumber',1)
					cmds.setAttr(self.extrude[1] + '.scale',self.taper)
					
					if self.autoAdd is True and self.extrude[0] not in self.targetObj:
							self.targetObj.append(self.extrude[0])
						
		# refresh viewport
		cmds.refresh(cv=True)
		
	def onDrag(self):
	
		# modifier
		self.mod = cmds.getModifiers()
		
		# positions
		currentPos = cmds.draggerContext(self.dragCtx, query=True, dragPoint=True)
		
		# camera far clip
		currentView = omui.M3dView().active3dView()
		camDP = om.MDagPath()
		
		currentView.getCamera(camDP)
		camFn = om.MFnCamera(camDP)
		farclip = camFn.farClippingPlane()
		
		# screen to world conversion
		worldPos, worldDir = utils().viewToWorld(currentPos[0],currentPos[1])
		
		
		closestHit = None
		closestObj = None
		for obj in self.targetObj:
			state, hit, fnMesh, facePtr, triPtr = utils().intersect(obj, worldPos, worldDir, farclip)
				
			if state is True:
				dif = [hit.x - worldPos[0],hit.y - worldPos[1],hit.z - worldPos[2]]
				distToCam = math.sqrt(math.pow(float(dif[0]),2) + math.pow(float(dif[1]),2) + math.pow(float(dif[2]),2))
				if closestHit == None:
					closestHit = distToCam
					closestObj = [state, hit, fnMesh, facePtr, triPtr]
				elif distToCam < closestHit:
					closestHit = distToCam
					closestObj = [state, hit, fnMesh, facePtr, triPtr]
		if closestObj is not None:
			state, hit, fnMesh, facePtr, triPtr = closestObj
			
			mHit = om.MPoint(hit)
			# get smooth normal
			normal = om.MVector()
			fnMesh.getClosestNormal(mHit, normal, om.MSpace.kWorld, None)
			
			tangent = utils().crossProduct(normal,self.worldUp)
			
			
			
			upAxis = utils().crossProduct(normal,tangent)
			
			# define transformation matrix
			matrix = [tangent.x,tangent.y,tangent.z,0,upAxis.x,upAxis.y,upAxis.z,0,normal.x,normal.y,normal.z,0,hit.x,hit.y,hit.z,0]
			
			# apply matrix
			dist = om.MVector( (hit.x - self.prevHit.x),(hit.y - self.prevHit.y),(hit.z - self.prevHit.z) )
			if utils().magnitude(dist) > self.step:
				if self.mod == 0:
					cmds.curve(self.loc,append=True,p=(hit.x,hit.y,hit.z))
			else:
				hit = self.prevHit
			
			
			if self.mesh is True:
					v1 = cmds.pointPosition(self.loc + '.cv[0]',w=True)
					v2 = cmds.pointPosition(self.loc + '.cv[1]',w=True)
					v = om.MVector(v2[0] - v1[0],v2[1] - v1[1],v2[2] - v1[2])
					v.normalize()
					cmds.setAttr(self.circle[1] + '.normalX',v.x)
					cmds.setAttr(self.circle[1] + '.normalY',v.y)
					cmds.setAttr(self.circle[1] + '.normalZ',v.z)
					
					
					if self.mod == 1:
						mag = utils().magnitude(dist) * self.bMult
						if dist.y < 0:
							mag = -mag
						currentValue = cmds.getAttr(self.circle[1] + '.radius')
						compVal = sorted((0.0001,currentValue + mag))[1]
						self.bRad = compVal
						cmds.setAttr(self.circle[1] + '.radius',compVal)
					
					if self.mod == 4:
						mag = utils().magnitude(dist) * self.bMult
						if dist.y < 0:
							mag = -mag
						currentValue = cmds.getAttr(self.extrude[1] + '.scale')
						compVal = sorted((0.0001,currentValue + mag))[1]
						self.taper = compVal
						cmds.setAttr(self.extrude[1] + '.scale',compVal)
			
			self.prevHit = hit
			# print cmds.timerX(st=self.timer)
			
			# refresh viewport
			currentView.refresh(False,True,False)
			# print normal.x, normal.y, normal.z
	
	def onRelease(self):
		pass
		
			
class utils():
	def __init__(self):
		pass
		
	def getDAGObject(self,dagstring):
		'''
		return the DAG Api object from the dagstring argument
		return None if the minimum checks on dagstring don't checkout
		'''
		sList = om.MSelectionList()
		meshDP = om.MDagPath()
		#sList.clear() #making sure to clear the content of the MSelectionList in case we are looping through multiple objects
		# om.MGlobal.getSelectionListByName(dagstring, sList)
		sList.add(dagstring)
		sList.getDagPath(0,meshDP)

		return meshDP;
		
	def viewToWorld(self,x,y):
		# get current view
		currentView = omui.M3dView().active3dView()
		
		# empty objects
		resultPt = om.MPoint()
		resultVtr = om.MVector()
		
		# conversion
		currentView.viewToWorld(int(x),int(y),resultPt,resultVtr)
		
		# return
		return [resultPt.x,resultPt.y,resultPt.z],[resultVtr.x,resultVtr.y,resultVtr.z]
		
	def intersect(self, dag, pos, dir, farclip):
		
		# mesh object
		targetDAGPath = self.getDAGObject(dag)
		meshObj = om.MFnMesh(targetDAGPath)
		
		# position FP
		posFP = om.MFloatPoint(pos[0],pos[1],pos[2])
		
		# dir FP
		dirFP = om.MFloatVector(dir[0],dir[1],dir[2])
		
		# empty objects
		
		hitFPoint = om.MFloatPoint()		# intersection
		hitFace = om.MScriptUtil()
		hitTri = om.MScriptUtil()
		hitFace.createFromInt(0)
		hitTri.createFromInt(0)
		
		hFacePtr = hitFace.asIntPtr()
		hTriPtr = hitTri.asIntPtr()
		
		hit = meshObj.closestIntersection( posFP,
									dirFP,
									None,
									None,
									True,
									om.MSpace.kWorld,
									farclip,
									True,
									None,
									hitFPoint,
									None,
									hFacePtr,
									hTriPtr,
									None,
									None)
									
		return hit, hitFPoint, meshObj, hitFace.getInt(hFacePtr), hitTri.getInt(hTriPtr)
		
	def crossProduct(self,vA,vB):
		vC = om.MVector(((vA.y*vB.z) - (vA.z*vB.y)) , ((vA.z*vB.x) - (vA.x*vB.z)), ((vA.x*vB.y) - (vA.y*vB.x)))
		vC.normalize()
		return vC
		
	def dotProduct(self,vA,vB):
		# vA.normalize()
		# vB.normalize()
		result = (vA.x * vB.x) + (vA.y * vB.y) + (vA.z * vB.z)
		return result
		
	def vectorAngle(self,vA,vB):
		scalar = self.dotProduct(vA,vB)
		mag = self.magnitude(vA) + self.magnitude(vB)
		angle = math.acos(scalar/mag)
		return angle
		
	def magnitude(self,v):
		magnitude = math.sqrt( math.pow(v.x,2) + math.pow(v.y,2) + math.pow(v.z,2) )
		return magnitude
		
class UI():
	def __init__(self):
		self.winName = "GF_CURVEONMESH_WIN"
		self.winTitle = "GF Curve on Mesh v2.0"
		
	def create(self):
		if cmds.window(self.winName,exists=True):
			cmds.deleteUI(self.winName)
		cmds.window(self.winName, title=self.winTitle)
		self.mainColumn = cmds.columnLayout()
		self.meshCbx = cmds.checkBox(label = 'Draw Mesh', value = False)
		self.bRadSlider = cmds.floatSliderGrp( label='Radius : ', field=True, columnWidth=(1, 100), min=0,max=10,value=1, pre = 1, fmn = 0, fmx = 9999 )
		self.baseMultSlider = cmds.floatSliderGrp( label='Base Drag Mult. : ', field=True, columnWidth=(1, 100), min=0,max=100,value=1, pre = 1, fmn = 0, fmx = 9999 )
		self.taperSlider = cmds.floatSliderGrp( label='Taper : ', field=True, columnWidth=(1, 100), min=0,max=1,value=1, pre = 2, fmn = 0, fmx = 9999 )
		self.taperMultSlider = cmds.floatSliderGrp( label='Taper Drag Mult. : ', field=True, columnWidth=(1, 100), min=0,max=100,value=.1, pre = 1, fmn = 0, fmx = 9999 )
		self.autoAddCbx = cmds.checkBox(label = 'Add current to Object list', value = False)
		self.stepSlider = cmds.floatSliderButtonGrp( label='Step : ', field=True, buttonLabel='Run', columnWidth=(1, 100), min=0,max=5,value=0.25, pre = 2, bc=self.run, fmn = 0, fmx = 9999 )
		
		# show window
		cmds.showWindow(self.winName)
		
	def run(self):
		step = cmds.floatSliderButtonGrp(self.stepSlider,q=True,value=True)
		mesh = cmds.checkBox(self.meshCbx,q=True, value = True)
		radius = cmds.floatSliderGrp(self.bRadSlider,q=True,value=True)
		bmult = cmds.floatSliderGrp(self.baseMultSlider,q=True,value=True)
		taper = cmds.floatSliderGrp(self.taperSlider,q=True,value=True)
		tmult = cmds.floatSliderGrp(self.taperMultSlider,q=True,value=True)
		autoAdd = cmds.checkBox(self.autoAddCbx,q=True, value = True)
		meshDrawCtx(cmds.ls(sl=True,l=True),step,mesh,radius,bmult,taper,tmult,autoAdd).run()