from localstack.utils.aws import aws_models
zUPfE=super
zUPfw=None
zUPfH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zUPfE(LambdaLayer,self).__init__(arn)
  self.cwd=zUPfw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,zUPfH,env=zUPfw):
  zUPfE(RDSDatabase,self).__init__(zUPfH,env=env)
 def name(self):
  return self.zUPfH.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,zUPfH,env=zUPfw):
  zUPfE(RDSCluster,self).__init__(zUPfH,env=env)
 def name(self):
  return self.zUPfH.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
