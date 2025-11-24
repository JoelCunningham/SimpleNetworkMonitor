import { ViewDeviceForm } from '#components/forms';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewDeviceForm', () => {
  let component: ViewDeviceForm;
  let fixture: ComponentFixture<ViewDeviceForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewDeviceForm],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewDeviceForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
