import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditOwnerForm } from './edit-owner-form';

describe('EditOwnerForm', () => {
  let component: EditOwnerForm;
  let fixture: ComponentFixture<EditOwnerForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditOwnerForm],
    }).compileComponents();

    fixture = TestBed.createComponent(EditOwnerForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
