
User / Admin / All :
Register($userdata){ };
AddPaymentMethod($userdata){  };
	RemovePaymentMethod($userdata){  };
	Login($member, $password){  };
	SendHelpMessage($message){  };
AddFriend($friend){  };	
DeleteFriend($friend){  };
PayFriend($friend){  };
PayInto($group, $amount){  };
CreateGroup($group, $password){  };
ViewGroups($member){  };
LeaveGroup($member){  };

Leader:
AddMember($group, $member){  };
DeleteMember($group, $member){  };
	GiveLeader($group, $member){  };
	SetGroupGoal($group, $member[ used to check rights ], $monetaryUnit){  };
	PollGroupGoal($group, $monetaryUnit){  };%possible idea 
ForceLeaveGroup($group, $moderator, $member){  };
TakePitch($group){  };% Takes the money in the group
Admin:	
	ViewMessages($member){  };
	ViewHelpMessages(){  };
	OverRide($self, $function($arguments){  };){  }; 
	ResetGroup($group){  };
	ResetMember($member){  };
