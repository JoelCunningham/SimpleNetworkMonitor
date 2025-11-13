import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditField } from './edit-field';

describe('EditField', () => {
  let component: EditField;
  let fixture: ComponentFixture<EditField>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditField],
    }).compileComponents();

    fixture = TestBed.createComponent(EditField);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
