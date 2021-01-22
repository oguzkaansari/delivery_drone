#include <ignition/math/Pose3.hh>
#include "gazebo/physics/physics.hh"
#include "gazebo/common/common.hh"
#include "gazebo/gazebo.hh"
#include <iostream>
#include <fstream>

using namespace std;
using namespace ignition::math;
namespace gazebo
{
  class CityPlugin : public WorldPlugin
  {
   
    public: void Load(physics::WorldPtr _world, sdf::ElementPtr _sdf)
            {
		ofstream file("locations.txt");
		auto models = _world -> Models();
		int count = _world -> ModelCount();
		printf("%d", count);		
		
		for(int i = 0; i < count; i++){
			auto name = models[i] -> GetName();
			auto pose = models[i] -> WorldPose();
			Vector3<double> position = pose.Pos();
 			double pos[3] = {position.X(), position.Y(), position.Z()};
			
			if (name.rfind("asphalt", 0) != 0) {
				file << name << ", " << pos[0] << ", " << pos[1] << ", " << pos[2] << "\n";
			}
			
		}
		  file.close();

            }
	
    	
  };
  GZ_REGISTER_WORLD_PLUGIN(CityPlugin)
}


