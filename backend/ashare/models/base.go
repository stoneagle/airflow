package models

import "time"

type GeneralWithDeleted struct {
	Id        int       `xorm:"pk autoincr" form:"Id" json:"Id" structs:"id,omitempty"`
	CreatedAt time.Time `xorm:"created comment('创建时间')" form:"CreatedAt" json:"CreatedAt" structs:"created_at,omitempty"`
	UpdatedAt time.Time `xorm:"updated comment('修改时间')" form:"UpdatedAt" json:"UpdatedAt" structs:"updated_at,omitempty"`
	DeletedAt time.Time `xorm:"deleted comment('软删除时间')" form:"DeletedAt" json:"DeletedAt" structs:"deleted_at,omitempty"`
}

type General struct {
	Id        int       `xorm:"pk autoincr" form:"Id" json:"Id" structs:"id,omitempty"`
	CreatedAt time.Time `xorm:"created comment('创建时间')" form:"CreatedAt" json:"CreatedAt" structs:"created_at,omitempty"`
	UpdatedAt time.Time `xorm:"updated comment('修改时间')" form:"UpdatedAt" json:"UpdatedAt" structs:"updated_at,omitempty"`
}

type GeneralWithoutId struct {
	CreatedAt time.Time `xorm:"created comment('创建时间')" form:"CreatedAt" json:"CreatedAt" structs:"created_at,omitempty"`
	UpdatedAt time.Time `xorm:"updated comment('修改时间')" form:"UpdatedAt" json:"UpdatedAt" structs:"updated_at,omitempty"`
}
