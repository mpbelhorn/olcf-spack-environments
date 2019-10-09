from spack import *
import shutil

class SparkOnDemand(Package):
    """Description"""

    homepage = "https://code.ornl.gov/d3s/spark_on_demand"
    url      = "git@code.ornl.gov:d3s/spark_on_demand.git"

    version('2.0.2',git='https://code.ornl.gov/d3s/spark_on_demand.git')

    depends_on('spark@2.0.2+hadoop')

    def install(self, spec, prefix):
      spark_prefix = spec['spark'].prefix
      ln = which('ln')
      mkdir = which('mkdir')
      chmod = which('chmod')
      mkdir(prefix+'/bin')
      mkdir(prefix+'/sbin')
      shutil.copyfile('spark_setup.py', prefix+'/bin/spark_setup.py')
      shutil.copyfile('spark_deploy.py', prefix+'/sbin/spark_deploy.py')
      chmod('+x',prefix+'/bin/spark_setup.py')
      chmod('+x',prefix+'/sbin/spark_deploy.py')
      ln('-sf', prefix+'/bin/spark_setup.py', spark_prefix+'/bin/spark_setup.py')
      ln('-sf', prefix+'/sbin/spark_deploy.py', spark_prefix+'/sbin/spark_deploy.py')
      return 0
