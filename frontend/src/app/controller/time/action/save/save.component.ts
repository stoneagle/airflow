import { Component, OnInit, Output, Input, EventEmitter, Inject, forwardRef } from '@angular/core';
import { EJ_DATETIMEPICKER_COMPONENTS }                                       from 'ej-angular2/src/ej/datetimepicker.component';
import { EJ_DROPDOWNLIST_COMPONENTS }                                         from 'ej-angular2/src/ej/dropdownlist.component';
import { EJ_SCHEDULE_COMPONENTS }                                             from 'ej-angular2/src/ej/schedule.component';

import { QuestTeam }          from '../../../../model/time/quest';
import { Task, TaskSettings } from '../../../../model/time/task';
import { Action }             from '../../../../model/time/action';
import { Project }            from '../../../../model/time/project';
import { SessionUser }        from '../../../../model/base/sign';
import { ActionService  }     from '../../../../service/time/action.service';
import { TaskService  }       from '../../../../service/time/task.service';
import { ProjectService  }    from '../../../../service/time/project.service';
import { SignService  }       from '../../../../service/system/sign.service';
import { ShellComponent }     from '../../../../base/shell/shell.component';

@Component({
  selector: 'time-action-save',
  templateUrl: './save.component.html',
  styleUrls: ['./save.component.css']
})


export class ActionSaveComponent implements OnInit {
  action: Action = new Action();
  modelOpened: boolean = false;
  tasks: Task[] = [];
  taskGroupBy = (item) => item.Project.Name;

  @Output() save = new EventEmitter<Action>();

  constructor(
    private taskService: TaskService,
    private taskSettings: TaskSettings,
    private projectService: ProjectService,
    private signService: SignService,
    private actionService: ActionService,
    @Inject(forwardRef(() => ShellComponent))
    private shell: ShellComponent,
  ) { }

  ngOnInit() {
    this.action = new Action();
    this.action.StartDate = new Date();
    this.action.EndDate = new Date();
  }

  initTasks(userId: number): void {
    this.taskService.ListByUser(userId).subscribe(tasks => {
      tasks.forEach( (item, index) => {
        if (item.Status == this.taskSettings.Status.Done) {
          tasks.splice(index, 1);
        }
      });
      this.tasks = tasks;
    })
  }

  NewWithDate(startDate: Date, endDate: Date): void {
    this.initTasks(this.shell.currentUser.Id);
    this.action = new Action();
    this.action.StartDate = startDate;
    this.action.EndDate = endDate;
    this.action.UserId = this.shell.currentUser.Id;
    this.modelOpened = true;
  }

  NewWithTask(taskId: number): void {
    this.initTasks(this.shell.currentUser.Id);
    this.action = new Action();
    this.action.Task.Ids = [taskId];
    this.action.StartDate = new Date();
    this.action.EndDate = new Date();
    this.action.UserId = this.shell.currentUser.Id;
    this.modelOpened = true;
  }

  New(id?: number): void {
    this.initTasks(this.shell.currentUser.Id);
    if (id) {
      this.actionService.Get(id).subscribe(res => {
        this.action = res;
        this.action.Task.Ids = [this.action.TaskId];
        this.action.UserId = this.shell.currentUser.Id;
        this.action.StartDate = new Date(this.action.StartDate);
        this.action.EndDate = new Date(this.action.EndDate);
        this.modelOpened = true;
      })
    } else {
      this.action = new Action();
      this.action.StartDate = new Date();
      this.action.EndDate = new Date();
      this.action.UserId = this.shell.currentUser.Id;
      this.modelOpened = true;
    }
  }            

  Submit(): void {
    if ((this.action.Task.Ids == undefined) || (this.action.Task.Ids.length != 1)) {
      return;
    }
    this.action.TaskId = this.action.Task.Ids[0];
    let time = this.action.EndDate.getTime() - this.action.StartDate.getTime();
    this.action.Time = time / 1000 / 60;
    if (this.action.Id == null) {
      this.actionService.Add(this.action).subscribe(res => {
        this.UpdateTaskStatus(this.action.Task)
        this.action.Id = res.Id;
        this.save.emit(this.action);
        this.modelOpened = false;
      })
    } else {
      this.actionService.Update(this.action).subscribe(res => {
        this.UpdateTaskStatus(this.action.Task)
        this.save.emit(this.action);
        this.modelOpened = false;
      })
    }
  }

  UpdateTaskStatus(task: Task): void {
    if (task.Status != this.taskSettings.Status.Done) {
      return;
    }
    if (task.Status != this.taskSettings.Status.Progress) {
      task.Status = this.taskSettings.Status.Progress;
      this.taskService.Update(task).subscribe(res => {
        return;
      })
    }
  }
}
