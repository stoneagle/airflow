import { Basic }    from '../base/basic';
import { Area }     from './area';
import { Resource } from './resource';
import { Task }     from './task';
import { Field }    from './field';

export class TreeGrid extends Basic {
  Id: number;
  Name: string;
  Parent: string;
  ParentId: number;
  IsParent: boolean;
  Children: TreeGrid[];
  constructor (json?: any) {
    if (json != undefined) {
      super(json)
    } else {
      this.Children = [];
    }
  }
}

export class Gantt extends Basic {
  Id: number;
  Name: string;
  Relate: string;
  RelateId: number;
  StartDate: Date;
  EndDate: Date;
  Progress: number;
  Duration: number;
  Expended: boolean;
  Parent: number;
  Status: number;
  Color: string;
  Children: Gantt[];
  constructor (json?: any) {
    if (json != undefined) {
      super(json)
    } else {
      this.Children = [];
    }
  }
}

export class Schedule extends Basic {
  Id: number;
  Name: string;
  StartDate: Date;
  EndDate: Date;
  FieldId: string;
  AllDay: boolean;
  Recurrence: boolean;
  Field: Field;
  Area: Area;
  Resource: Resource;
  Task: Task;
}

export class Kanban extends Basic {
	Id          :number
	Name        :string
	Desc        :string
	Tags        :string
	Status      :number
	StatusName  :string
	ProjectId   :number
	ProjectName :string
	ResourceId  :number
	ResourceName:string
	FieldId     :number
	FieldName   :string
  Closed      :boolean
}

export class SyncfusionSettings {
  public GanttStatus = {
    Wait: "wait",
    Finish: "finish",
  };
  public GanttLevel = {
    Quest: "quest",
    Project: "project",
    Task: "task",
  };
}


