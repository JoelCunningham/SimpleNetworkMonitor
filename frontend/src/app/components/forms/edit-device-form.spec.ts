import { EditDeviceForm } from '#components/forms';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditDeviceForm', () => {
  let component: EditDeviceForm;
  let fixture: ComponentFixture<EditDeviceForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDeviceForm],
    }).compileComponents();

    fixture = TestBed.createComponent(EditDeviceForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
