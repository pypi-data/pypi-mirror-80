from localstack.utils.aws import aws_models
FDPXr=super
FDPXV=None
FDPXU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  FDPXr(LambdaLayer,self).__init__(arn)
  self.cwd=FDPXV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,FDPXU,env=FDPXV):
  FDPXr(RDSDatabase,self).__init__(FDPXU,env=env)
 def name(self):
  return self.FDPXU.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,FDPXU,env=FDPXV):
  FDPXr(RDSCluster,self).__init__(FDPXU,env=env)
 def name(self):
  return self.FDPXU.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
